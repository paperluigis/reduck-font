from sys import argv
import os

sfd_src = argv[1]
sfd_dest = argv[2]

ff = fontforge.open(sfd_src)
ff.save(sfd_dest)
