db.sensor_readings.aggregate([
  {
    $setWindowFields: {
      partitionBy: "$sensorId",
      sortBy: { timestamp: 1 },
      output: {
        rollingAvg: {
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
      rollingAvg: { $gt: 75 }
    }
  }
])
