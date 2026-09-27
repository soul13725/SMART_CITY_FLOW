Write-Host "MongoDB Setup Database Script"
Write-Host "This requires mongosh to be installed locally."
mongosh --eval "use smart_city; db.createCollection('traffic_events'); db.traffic_events.createIndex({event_id: 1}, {unique: true});"
