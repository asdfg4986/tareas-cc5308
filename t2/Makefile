PYTHON  := python3
TARGET  := sapo
SCRIPT  := sapo.py

.PHONY: all clean run check

all: $(TARGET)

$(TARGET): $(SCRIPT)
	cp $(SCRIPT) $(TARGET)
	chmod +x $(TARGET)

run: $(TARGET)
	./$(TARGET) --help

check:
	$(PYTHON) -m py_compile $(SCRIPT)

clean:
	rm -f $(TARGET) __pycache__/*.pyc
	rmdir __pycache__ 2>/dev/null || true
