db.sensor_readings.aggregate([
  {
    $group: {
      _id: {
        day: { $dateTrunc: { date: "$timestamp", unit: "day" } },
        sensorId: "$sensorId"
      },
      avgReading: { $avg: "$reading" },
      maxReading: { $max: "$reading" },
      minReading: { $min: "$reading" },
      count: { $sum: 1 }
    }
  },
  {
    $sort: { "_id.day": -1 }
  }
])
