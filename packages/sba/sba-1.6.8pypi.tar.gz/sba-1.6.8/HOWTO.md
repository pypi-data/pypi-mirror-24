To install this library, you will need to first install the sba library (libsba.so); then the sba projections library (libsbaprojs.so) **before** installing the Python wrapper using setup.py. 

  1. Obtain sba (current version 1.6) from [http://www.ics.forth.gr/~lourakis/sba]

  2. You will need to alter the Makefile in order to build the library as a shared object.  See the example Makefile; or add the following lines to Makefile using a text editor:
```
libsba.so: 
	$(CC) -fPIC -c sba.h sba_levmar.c sba_levmar_wrap.c sba_lapack.c sba_crsm.c sba_chkjac.c
	$(CC) -shared -o libsba.so $(OBJS) -llapack -lblas
```

  3. Build the sba library as a shared object with make using the following at the command prompt:
```
make libsba.so
```

  4. This should result in a file libsba.so that provides the compiled shared object that can be called from Python.  As adminstrator/sudo, place libsba.so in /usr/local/lib, create a symbolic link for it, copy the header too, and update the shared library information (default locations for Ubuntu given below; on Mac o Windows you will need to use different locations):
```
cp libsba.so /usr/local/lib/libsba.so.1.6
chmod a-x /usr/local/lib/libsba.so.1.6
ln -s /usr/local/lib/libsba.so.1.6 /usr/local/lib/libsba.so
cp sba.h /usr/local/include
ldconfig
```

  5. Next, obtain libsbaprojs using Mercurial to clone from [https://bitbucket.org/devangel77b/libsbaprojs] or [ssh://hg@bitbucket.org/devangel77b/libsbaprojs]:
```
hg clone ssh://hg@bitbucket.org/devangel77b/libsbaprojs
```
Install it by following the instructions provided with it.  You will run make to create libsbaprojs.so and then copy it, and the associated headers, into the same places you put libsba.so and sba.h.

  6. After libsba and libsbaprojs are available, you can install the Python sba code using the following (as administrator or sudo): 
```
python setup.py --install
```

  7. If building for a Mac, you may wish to use .dylib extension rather than .so; you will also want to modify the corresponding lines of code (e.g. ```libsba = ctypes.CDLL("libsba.dylib")```).
