#include <iostream>
#include <fstream>
#include "main.hpp"

using namespace std;

// Loads block from IO input stream
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

// Saves block to IO output stream
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

void find_new_collision(const uint32 IV[], uint32 msg1block0[], uint32 msg1block1[], uint32 msg2block0[], uint32 msg2block1[], bool verbose)
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

int main()
{
	ifstream ifs("/Users/fproulx/Desktop/msg1", ios::binary);
	uint32 msg1block0[16];
	uint32 msg1block1[16];
	load_block(ifs, msg1block0);
	load_block(ifs, msg1block1);

	uint32 msg2block0[16];
	uint32 msg2block1[16];
	compute_msg2_from_msg1(msg1block0, msg1block1, msg2block0, msg2block1);

	ofstream ofs2("/Users/fproulx/Desktop/msg2", ios::binary);
	save_block(ofs2, msg2block0);
	save_block(ofs2, msg2block1);
}
