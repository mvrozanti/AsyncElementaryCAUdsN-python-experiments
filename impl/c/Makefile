src = $(wildcard *.c)
obj = $(src:.c=.o)
aeca: $(obj)
	$(CC) -o $@ $^
	rm $(obj)
.PHONY: clean
clean:
	rm -f $(obj) aeca

