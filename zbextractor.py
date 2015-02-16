import argparse
import os
import sys
import uuid

def buffer_window_read(f, buf):

   if buf != '':
      buf[0] = buf[1]
      buf[1] = buf[2]
      buf[2] = buf[3]
      buf[3] = f.read(1)
   else:
      buf = []
      buf.append(f.read(1))
      buf.append(f.read(1))
      buf.append(f.read(1))
      buf.append(f.read(1))
   
   return buf

def extractJpegs(tnfile):

   bFound = False
   
   if os.path.isfile(tnfile):
   
      #if we need a directory name, create it here
      dirname = tnfile.split('.',1)[0] + '-' + str(uuid.uuid4())

      f = open(tnfile, 'rb')

      tncount = 0
      endcount = 0

      buf = ''

      file_len = os.path.getsize(f.name)

      JPGHead = '\xFF\xD8';
      JPGTail = '\xFF\xD9';

      while f.tell() < file_len:
         buf = buffer_window_read(f, buf)
         fbytes = b"".join(buf[0:2])
         if fbytes == JPGHead:
         
            #Create a folder to store jpegs
            if bFound == False: 
               if not os.path.exists(dirname):
                  os.makedirs(dirname)
                  bfound = True
            
            tncount+=1
            file = []
            file = buf
            buf = ''
            eofJPG = False
            while eofJPG == False:
               buf = buffer_window_read(f, buf)
               fbytes = b"".join(buf[0:2])
               if fbytes == JPGTail:
                  file.append(buf[0])
                  file.append(buf[1])
                  eofJPG=True
                  buf = ''
                  jpg = open(dirname + '\image-' + str(tncount).zfill(4) + '.jpg', 'wb')
                  jpg.write(b"".join(file[0:]))
                  jpg.close()
               else:
                  file.append(buf[0])

      f.close()
      sys.stdout.write(str(tncount) + " JPEGs discovered." + "\n")
   else:
      sys.stdout.write("Warning: Filename provided does not point to a file.")

def main():

   #	Usage: 	--info [ZbThumbnail.info]

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Extract JPG from ZbThumbnail.info files. NOTE: May also be applicable to Thumbs.db at users own risk.')
   parser.add_argument('--info', help='Optional: Single zbthumbnail.info file to read.', default=False)

   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   if args.info:
      extractJpegs(args.info)
   
   else:
      sys.exit(1)

if __name__ == "__main__":
   main()
