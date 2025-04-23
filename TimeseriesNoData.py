const cutoff = new Date(Date.now() - 10 * 60 * 1000); // 10 minutes ago

db.sensor_readings.aggregate([
  {
    $group: {
      _id: "$sensorId",
      lastSeen: { $max: "$timestamp" }
    }
  },
  {
    $match: {
      lastSeen: { $lt: cutoff }
    }
  }
])
