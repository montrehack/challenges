import os
import re
import sys
import base64
import numpy as np
import binascii
from PIL import Image

if __name__=='__main__':
	if(len(sys.argv) == 1):
		sys.exit(1)

	phpSessionID = sys.argv[1]

	# The modulus is there because otherwise it crashes since the number is too high.
	np.random.seed(int(binascii.hexlify(phpSessionID.encode("utf-8")),16)%4294967295)

	arr = np.random.randint(0, 255, (np.random.randint(100,500), np.random.randint(100,500), 3))
	img = Image.fromarray(arr,'RGB')
	
	# Avoid path traversal and bad voodoo stuff
	if(re.match("^[a-zA-Z0-9,-]+$",phpSessionID)):
		filename = phpSessionID
		pathname = "/tmp/{filename}.{extension}"
		img.save(pathname.format(filename=filename, extension="png"))

		try:
			content = b"data:image/jpeg;base64," + base64.standard_b64encode(open(pathname.format(filename=filename, extension="png"), 'rb').read())

			# Write the content to a txt file so that the PHP can take it and put it as an image with data://.
			with open(pathname.format(filename=filename, extension="txt"),'w') as f:
				f.write(content.decode())
				f.close()

		finally:
			os.remove(pathname.format(filename=filename, extension="png"))
	else:
		sys.exit(1)