/*
Modified  fastcoll
*/

#include <iostream>
#include <fstream>
#include <time.h>

#include "main.hpp"

using namespace std;

// MD5 IV (from specification)
const uint32 MD5IV[] = { 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476 };

// IO file functions
unsigned load_block(istream& i, uint32 block[]);
void save_block(ostream& o, const uint32 block[]);

// MD5 Collision compute
void find_new_collision(const uint32 *IV, uint32 *msg1block0, uint32 *msg1block1, uint32 *msg2block0, uint32 *msg2block1, bool verbose = false);
void compute_msg2_from_msg1(uint32 msg1block0[], uint32 msg1block1[], uint32 msg2block0[], uint32 msg2block1[]);

#include <sstream>
#include <string>
#include <utility>
#include <boost/filesystem/operations.hpp>
#include <boost/program_options.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/timer.hpp>
#include <boost/cstdint.hpp>

typedef boost::uint64_t uint64;

namespace fs = boost::filesystem;
namespace po = boost::program_options;
using boost::lexical_cast;

int main(int argc, char** argv)
{
#if 1
	if (argc == 3) {
		ifstream ifs(argv[1], ios::binary);
		uint32 msg1block0[16];
		uint32 msg1block1[16];
		load_block(ifs, msg1block0);
		load_block(ifs, msg1block1);

		uint32 msg2block0[16];
		uint32 msg2block1[16];
		compute_msg2_from_msg1(msg1block0, msg1block1, msg2block0, msg2block1);

		ofstream ofs2(argv[2], ios::binary);
		save_block(ofs2, msg2block0);
		save_block(ofs2, msg2block1);
		
		return 0;
	} else {
		return 1;
	}
#else
	seed32_1 = uint32(time(NULL));
	seed32_2 = 0x12345678;

	uint32 IV[4] = { MD5IV[0], MD5IV[1], MD5IV[2], MD5IV[3] };

	string outfn1 = "msg1.bin";
	string outfn2 = "msg2.bin";
	string ihv;
	string prefixfn;
	bool verbose = true;

	cout <<
		"MD5 collision generator v1.5\n"
		"by Marc Stevens (http://www.win.tue.nl/hashclash/)\n"
		<< endl;

	try
	{
		boost::timer runtime;

		po::options_description desc("Allowed options");
		desc.add_options()
			("help,h", "Show options.")
			("quiet,q", "Be less verbose.")
			("ihv,i", po::value<string>(&ihv), "Use specified initial value. Default is MD5 initial value.")
			("prefixfile,p", po::value<string>(&prefixfn), "Calculate initial value using given prefixfile. Also copies data to output files.")			
			("out,o", po::value<vector<string> >()->multitoken(), "Set output filenames. This must be the last option and exactly 2 filenames must be specified. \nDefault: -o msg1.bin msg2.bin")
			;

		po::options_description hidden;
		hidden.add_options()
			("testmd5iv", "Endlessly time collision generation using MD5 initial value.")
			("testrndiv", "Endlessly time collision generation using arbitrary random initial values.")
			("testreciv", "Endlessly time collision generation using recommended random initial values.")
			("testall", "Endlessly time collision generation for each case.")
			;

		po::options_description cmdline;
		cmdline.add(desc).add(hidden);
		po::positional_options_description p;
		p.add("prefixfile", 1);
		po::variables_map vm;
		po::store(po::command_line_parser(argc, argv).options(cmdline).positional(p).run(), vm);
		po::notify(vm);

		if (vm.count("quiet"))
			verbose = false;

		if (vm.count("help") || argc == 1) {
			cout << desc << endl;
			return 1;
		}

		if (vm.count("prefixfile"))
		{
			unsigned l = prefixfn.size();
			if (l >= 4 && prefixfn[l-4]=='.' && prefixfn[l-3]!='.' && prefixfn[l-2]!='.' && prefixfn[l-1]!='.')
			{
				outfn1 = prefixfn.substr(0, l-4) + "_msg1" + prefixfn.substr(l-4);
				outfn2 = prefixfn.substr(0, l-4) + "_msg2" + prefixfn.substr(l-4);
				unsigned i = 1;
				while ( fs::exists(fs::path(outfn1)) 
					 || fs::exists(fs::path(outfn2)))
				{
					outfn1 = prefixfn.substr(0, l-4) + "_msg1_" + lexical_cast<string>(i) + prefixfn.substr(l-4);
					outfn2 = prefixfn.substr(0, l-4) + "_msg2_" + lexical_cast<string>(i) + prefixfn.substr(l-4);
					++i;
				}
			}
		}

		if (vm.count("out"))
		{
			vector<string> outfns = vm["out"].as< vector<string> >();
			if (outfns.size() != 2)
			{
				cerr << "Error: exactly two output filenames should be specified." << endl;
				return 1;
			}
			outfn1 = outfns[0];
			outfn2 = outfns[1];
		}

		if (verbose)
			cout << "Using output filenames: '" << outfn1 << "' and '" << outfn2 << "'" << endl;
		ofstream ofs1(outfn1.c_str(), ios::binary);
		if (!ofs1)
		{
			cerr << "Error: cannot open outfile: '" << outfn1 << "'" << endl;
			return 1;
		}
		ofstream ofs2(outfn2.c_str(), ios::binary);
		if (!ofs2)
		{
			cerr << "Error: cannot open outfile: '" << outfn2 << "'" << endl;
			return 1;
		}

		if (vm.count("prefixfile"))
		{
			if (verbose)
				cout << "Using prefixfile: '" << prefixfn << "'" << endl;
			ifstream ifs(prefixfn.c_str(), ios::binary);
			if (!ifs)
			{
				cerr << "Error: cannot open inputfile: '" << prefixfn << "'" << endl;
				return 1;
			}
			uint32 block[16];
			while (true)
			{
				unsigned len = load_block(ifs, block);
				if (len)
				{
					save_block(ofs1, block);
					save_block(ofs2, block);
					md5_compress(IV, block);
				} else
					break;
			}
		}
		else
		{
			if (vm.count("ihv") == 0)
				ihv = "0123456789abcdeffedcba9876543210";
			if (ihv.size() != 32)
			{
				cerr << "Error: an initial value must be specified as a hash value of 32 hexadecimal characters." << endl;
				return 1;
			} else
			{
				uint32 c;
				for (unsigned i = 0; i < 4; ++i)
				{
					IV[i] = 0;
					for (unsigned b = 0; b < 4; ++b)
					{
						stringstream ss;
						ss << ihv.substr(i*8+b*2,2);
						ss >> hex >> c;					
						IV[i] += c << (b*8);
					}
				}

			}
		}
		if (verbose)
		{
			cout << "Using initial value: " << hex;
			unsigned oldwidth = cout.width(2);
			char oldfill = cout.fill('0');
			
			for (unsigned i = 0; i < 4; ++i)
			{
				for (unsigned b = 0; b < 4; ++b)
				{
					cout.width(2);
					cout.fill('0');
					cout << ((IV[i]>>(b*8))&0xFF);
				}
			}
			cout.width(oldwidth);
			cout.fill(oldfill);
			cout << dec << endl;
		}

		if (verbose)
			cout << endl;

		uint32 msg1block0[16];
		uint32 msg1block1[16];
		uint32 msg2block0[16];
		uint32 msg2block1[16];
		find_new_collision(IV, msg1block0, msg1block1, msg2block0, msg2block1, true);

		save_block(ofs1, msg1block0);
		save_block(ofs1, msg1block1);
		save_block(ofs2, msg2block0);
		save_block(ofs2, msg2block1);
		if (verbose)
			cout << "Running time: " << runtime.elapsed() << " s" << endl;
		return 0;
	} catch (exception& e)
	{
		cerr << "\nException caught:\n" << e.what() << endl;
		return 1;
	} catch (...)
	{
		cerr << "\nUnknown exception caught!" << endl;
		return 1;
	}
#endif
}

unsigned load_block(istream& i, uint32 block[])
{
	unsigned len = 0;
	char uc;
	for (unsigned k = 0; k < 16; ++k)
	{
		block[k] = 0;
		for (unsigned c = 0; c < 4; ++c)
		{
			i.get(uc);
			if (i) 
				++len;
			else
				uc = 0;
			block[k] += uint32((unsigned char)(uc))<<(c*8);
		}
	}
	return len;
}

void save_block(ostream& o, const uint32 block[])
{
	for (unsigned k = 0; k < 16; ++k)
		for (unsigned c = 0; c < 4; ++c)
			o << (unsigned char)((block[k] >> (c*8))&0xFF);
}

// Efficiently compute MD5 collision of given a specially crafted Wang-type message based on fixed IV
void compute_msg2_from_msg1(uint32 msg1block0[], uint32 msg1block1[], uint32 msg2block0[], uint32 msg2block1[])
{
	for (int t = 0; t < 16; ++t)
	{
		msg2block0[t] = msg1block0[t];
		msg2block1[t] = msg1block1[t];
	}
	msg2block0[4] += 1 << 31; msg2block0[11] += 1 << 15; msg2block0[14] += 1 << 31;
	msg2block1[4] += 1 << 31; msg2block1[11] -= 1 << 15; msg2block1[14] += 1 << 31;
}

void find_new_collision(const uint32 *IV, uint32 *msg1block0, uint32 *msg1block1, uint32 *msg2block0,
						uint32 *msg2block1, bool verbose)
{
	if (verbose)
		cout << "Generating first block: " << flush;
	find_block0(msg1block0, IV);

	uint32 IHV[4] = { IV[0], IV[1], IV[2], IV[3] };
	md5_compress(IHV, msg1block0);

	if (verbose)
		cout << endl << "Generating second block: " << flush;
	find_block1(msg1block1, IHV);

	for (int t = 0; t < 16; ++t)
	{
		msg2block0[t] = msg1block0[t];
		msg2block1[t] = msg1block1[t];
	}
	msg2block0[4] += 1 << 31; msg2block0[11] += 1 << 15; msg2block0[14] += 1 << 31;
	msg2block1[4] += 1 << 31; msg2block1[11] -= 1 << 15; msg2block1[14] += 1 << 31;
	if (verbose)
		cout << endl;
}
