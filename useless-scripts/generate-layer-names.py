e=[]

# ascii
e.extend(f"capital {k}" for k in "abcdefghijklmnopqrstuvwxyz")
e.extend(["left bracket","backslash","right bracket","caret","underscore"]) # [\]^_
e.extend(f"small {k}" for k in "abcdefghijklmnopqrstuvwxyz")
e.extend(["left brace","pipe","right brace","tilde"]) # {|}~

for p, j in enumerate(e):
	print(f"""<g inkscape:groupmode="layer" id="layer{p+12}" inkscape:label="{j}" style="display:none"></g>""")
