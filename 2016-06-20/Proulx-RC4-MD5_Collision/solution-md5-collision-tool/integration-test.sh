rm test-vectors/prefix
rm test-vectors/suffix
rm test-vectors/*.trim
rm test-vectors/*.computed
rm test-vectors/*.test

md5 test-vectors/*.full
shasum test-vectors/*.full

head -c 64 test-vectors/source.full > test-vectors/prefix
tail -c 543 test-vectors/source.full > test-vectors/suffix

head -c 192 test-vectors/source.full | tail -c 128 > test-vectors/source.trim
head -c 192 test-vectors/target.full | tail -c 128 > test-vectors/target.trim

./fastcoll test-vectors/source.trim test-vectors/target.trim.computed

cat test-vectors/prefix test-vectors/source.trim test-vectors/suffix > test-vectors/source.test
cat test-vectors/prefix test-vectors/target.trim.computed test-vectors/suffix > test-vectors/target.test

md5 test-vectors/*.test
shasum test-vectors/*.test