db.sensor_readings.find({
  timestamp: {
    $gte: new Date(Date.now() - 5 * 60 * 1000),  // 5 minutes ago
    $lte: new Date()
  },
  reading: { $gt: 70 }
})
