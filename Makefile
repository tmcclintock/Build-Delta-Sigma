OBJS = src/xi_nfw/xi_nfw.o src/sigma_r/sigma_r.o src/sigma_r/sigma_r_at_r.o src/delta_sigma/delta_sigma.o src/delta_sigma/delta_sigma_at_r.o src/miscentered_sigma_r/miscentered_sigma_r.o src/miscentered_sigma_r/miscentered_sigma_r_at_r.o src/miscentered_delta_sigma/miscentered_delta_sigma.o src/miscentered_delta_sigma/miscentered_delta_sigma_at_r.o src/wrapper/wrapper.o

CC = gcc
ifdef ALONE
ifeq ($(ALONE),yes)
$(info Building C stand-alone executable)
EXEC = main.exe
CFLAGS = 
OFLAGS = 
endif
else
$(info Building shared library)
EXEC = ./src/wrapper/Build_Delta_Sigma.so
CFLAGS = -fPIC
OFLAGS = -shared 
#-W1,-soname=$(EXEC)
endif

#Note the paths to GSL
INCL = -I/$(GSLI) -fopenmp -O2
LIBS = -lgsl -lgslcblas -L/$(GSLL) -lm -fopenmp -O2
.SUFFIXES : .c .o
%.o: %.c
	$(CC) $(CFLAGS) $(INCL) -c $< -o $@

$(EXEC): $(OBJS)
	$(CC) $(OFLAGS) $(OBJS) $(LIBS) -o $(EXEC)

#$(OBJS): $(INCL)

.PHONY : clean

clean:
	rm -f $(OBJS) main.exe $(EXEC)
	rm -f *~
