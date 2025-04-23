db.sensor_readings.aggregate([
  {
    $match: {
      sensorId: "sensor_1",
      timestamp: {
        $gte: ISODate("2025-04-23T09:00:00Z"),
        $lte: ISODate("2025-04-23T10:00:00Z")
      }
    }
  },
  {
    $group: {
      _id: {
        timestamp: {
          $dateTrunc: {
            date: "$timestamp",
            unit: "minute"
          }
        }
      },
      avgReading: { $avg: "$reading" }
    }
  },
  {
    $densify: {
      field
