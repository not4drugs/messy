from hypothesis import strategies

message = strategies.text().map(str.encode)
