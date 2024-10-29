import io


def last_lines(file_path, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """Retorna as linhas de um arquivo txt na ordem contraria."""
    with open(file_path, "rb") as f:
        f.seek(0, io.SEEK_END)
        file_size = f.tell()
        buffer_memory = b""

        for offset in range(file_size, 0, -buffer_size):
            read_size = min(buffer_size, offset)
            f.seek(offset - read_size)
            chunk = f.read(read_size) + buffer_memory
            rows = chunk.split(b"\n")
            buffer_memory = rows.pop(0)

            for row in reversed(rows):
                yield row.decode("utf-8") + "\n"

        if buffer_memory:
            yield buffer_memory.decode("utf-8") + "\n"


last_lines("bw_lines/my_file.txt")

for line in last_lines("bw_lines/my_file.txt"):
    print(line, end="")
