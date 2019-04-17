CREATE TABLE overview(
	current_day DATETIME PRIMARY KEY,
	current_value FLOAT,
	current_sentiment FLOAT,
	open_value FLOAT,
	open_sentiment FLOAT,
	value_change FLOAT,
	sentiment_change FLOAT,
	num_invested bigint
);

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
	"low" FLOAT,
	"high" FLOAT,
	"open_sentiment" FLOAT,
	"close_sentiment" FLOAT,
	"value_change" FLOAT,
	"sentiment_change" FLOAT
);