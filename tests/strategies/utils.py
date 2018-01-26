from hypothesis import strategies

messages = strategies.text().map(str.encode)
names = strategies.text(min_size=1)