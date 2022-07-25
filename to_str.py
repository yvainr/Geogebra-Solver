def to_str(self, nfacts, roots=True):
    out = ""

    if self.fact_type == "relation":
        a = type(self.objects[0])
        if type(self.objects[0]) != "task_parser.polygon":
            out += f"{self.objects[0]} относится к {self.objects[1]} с коэффицентом {self.value}"
            if roots:
                out += f" так как "
                nlist = []
                for root in self.root_facts:
                    nlist.append(f"{nfacts[root]}")
                out += ", ".join(nlist)
        else:
            out += f"{self.objects[0]} подобен {self.objects[1]} с коэффицентом {self.objects[0].size / self.objects[1].size}"
            if roots:
                out += f"так как"
                nlist = []
                for root in self.root_facts:
                    nlist.append(f"{nfacts[root]}")
                out += ", ".join(nlist)
    elif self.fact_type == "size":
        out += f"{self.objects[0]} равен {self.objects[0].size} по условию"
    elif self.fact_type == "additions":
        if len(self.objects) == 2:
            out += f"{self.objects[0]} равен {self.objects[0].size} как смежный с {self.objects[1]}"
            if roots:
                out += f"так как"
                nlist = []
                for root in self.root_facts:
                    nlist.append(f"{nfacts[root]}")
                out += ", ".join(nlist)
        elif len(self.objects) == 3:
            out += f"{self.objects[0]} равен {self.objects[0].size} как сумма {self.objects[1]} и {self.objects[2]}"
            if roots:
                out += f"так как"
                nlist = []
                for root in self.root_facts:
                    nlist.append(f"{nfacts[root]}")
                out += ", ".join(nlist)
    return out
