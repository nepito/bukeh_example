def get_match(df_possiession, match):
    team = df_possiession.columns[3]
    df_possiession = df_possiession.sort_values(by=[team])
    primer_partido = list(df_possiession.match)[match]
    primer_partido = primer_partido.split(" ")
    primer_partido.pop().replace(":", " a ")
    return " ".join(primer_partido).replace("-", "vs")
