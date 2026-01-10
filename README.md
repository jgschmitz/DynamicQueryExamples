# 🧠 DynamicQueryExamples
MongoDB is schema-flexible,  perfect for use cases like user-defined key-value pairs (e.g. consumer-defined form fields). But querying and sorting on these fields—especially when they’re dynamic—can be tricky.

✅ How MongoDB Can Handle It
Assume documents look like this:
```
{
  "_id": 1,
  "user_id": "abc123",
  "custom_fields": {
    "mood": "happy",
    "score": 9,
    "location": "NYC"
  }
}
```
If you want to search for users whose "mood" is "happy" and sort by "score", you can:

1. Project the Field and Compute a Value
Use $project to expose a dynamic field as a computed value:
```
db.collection.aggregate([
  {
    $match: {
      "custom_fields.mood": "happy"
    }
  },
  {
    $addFields: {
      scoreForSort: "$custom_fields.score"
    }
  },
  {
    $sort: { scoreForSort: -1 }
  }
])
```
This works well if the dynamic fields are not too deeply nested or complex.

2. Consider Schema Adjustments for Indexing
If performance is a concern and dynamic fields are common, consider storing custom fields as an array of key-value pairs:
```
"custom_fields": [
  { "key": "mood", "value": "happy" },
  { "key": "score", "value": 9 }
]
```
Then you can use an index on custom_fields.key and custom_fields.value.

Sorting becomes harder with this format unless you flatten during ingestion or use $arrayToObject tricks.

3. Can You Sort on Computed Values?
Yes—MongoDB 4.4+ supports sorting on computed fields from $addFields. But these won’t use indexes, so keep data volume in mind.

Part 2: Time-Series Query Within a Sliding Window
Let’s say you have a time-series collection like:
```
{
  "sensorId": "abc",
  "timestamp": ISODate("2025-04-23T10:00:00Z"),
  "reading": 75
}
```
And you want to find documents where the reading > 70 in a sliding 5-minute window.

✅ How MongoDB Can Handle It
Time-series queries rely on two parts:

Matching a time range

Filtering within that range
```
const now = new Date();
const fiveMinutesAgo = new Date(now.getTime() - 5 * 60000);

db.sensor_readings.find({
  timestamp: { $gte: fiveMinutesAgo, $lte: now },
  reading: { $gt: 70 }
})
```
📦 With Aggregation:
If you need to compute aggregates per sliding window (e.g., a moving average), use $setWindowFields (MongoDB 5.0+):
```
db.sensor_readings.aggregate([
  {
    $setWindowFields: {
      partitionBy: "$sensorId",
      sortBy: { timestamp: 1 },
      output: {
        avgReading: {
          $avg: "$reading",
          window: {
            range: [-5 * 60 * 1000, 0],
            unit: "millisecond"
          }
        }
      }
    }
  },
  {
    $match: {
      avgReading: { $gt: 70 }
    }
  }
])
```
This allows you to run a sliding window over your time-series data and filter based on windowed aggregations.
```
db.createCollection("sensor_readings", {
  timeseries: {
    timeField: "timestamp",
    metaField: "sensorId",
    granularity: "seconds"
  }
})
```
You can now run sliding window queries efficiently:

🔁 Sliding Window Query on Time-Series Collection
🔎 Example: Find sensor readings in last 5 minutes with reading > 70
```
db.sensor_readings.find({
  timestamp: {
    $gte: new Date(Date.now() - 5 * 60 * 1000),  // 5 minutes ago
    $lte: new Date()
  },
  reading: { $gt: 70 }
})
```
MongoDB Efficiently reads only relevant buckets
Uses the timeField index (automatically created)
Compresses older buckets for storage efficiency

📈 Advanced Use Case: Sliding Aggregates per Sensor
```
db.sensor_readings.aggregate([
  {
    $setWindowFields: {
      partitionBy: "$sensorId",
      sortBy: { timestamp: 1 },
      output: {
        avgReading: {
          $avg: "$reading",
          window: {
            range: [-5, 0],
            unit: "minute"
          }
        }
      }
    }
  },
  {
    $match: {
      avgReading: { $gt: 70 }
    }
  }
])
🔥 Bonus: This uses $setWindowFields on top of a time-series collection—MongoDB handles the internal bucket optimization for you.

