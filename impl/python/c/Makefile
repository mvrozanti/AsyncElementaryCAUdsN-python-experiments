src = $(wildcard *.c)
obj = $(src:.c=.o)
aeca: $(obj)
	$(CC) -o $@ $^ -lm -g
	rm $(obj)
.PHONY: clean
clean:
	rm -f $(obj) aeca

