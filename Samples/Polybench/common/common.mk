all:
	nvcc -g -G ${CUFILES} -I${PATH_TO_UTILS} -o ${EXECUTABLE} 
clean:
	rm -f *~ *.exe