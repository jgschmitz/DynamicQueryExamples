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
