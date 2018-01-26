from hypothesis import strategies

messages = strategies.text().map(str.encode)
