CREATE TABLE assets(
	ticker varchar PRIMARY KEY,
	sentiment FLOAT,
	price FLOAT,
	shares bigint
);

CREATE TABLE history(
	"day" DATETIME,
	"open" FLOAT,
	"close" FLOAT,
	"open_sentiment" FLOAT,
	"close_sentiment" FLOAT,
	"value_change" FLOAT,
	"sentiment_change" FLOAT,
	"num_invested" bigint
);