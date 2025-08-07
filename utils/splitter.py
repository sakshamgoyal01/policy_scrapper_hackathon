def split_into_clauses(clauses: list[dict], max_len=800):
    chunks = []
    current = {"number": None, "text": ""}
    for clause in clauses:
        txt = clause["text"]
        if len(current["text"]) + len(txt) < max_len:
            current["number"] = current["number"] or clause["number"]
            current["text"] += "\n" + txt
        else:
            chunks.append(current)
            current = {"number": clause["number"], "text": txt}
    if current["text"]:
        chunks.append(current)
    return chunks

