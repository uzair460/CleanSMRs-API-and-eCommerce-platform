from marshmallow import Schema, fields

class ObservationSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Str(required=True)
    time = fields.Str(required=True)
    timezone_offset = fields.Str(required=True)
    coordinates = fields.Str(required=True)
    water_temp = fields.Float()
    air_temp = fields.Float()
    humidity = fields.Float()
    wind_speed = fields.Float()
    wind_direction = fields.Float()
    precipitation = fields.Float()
    haze = fields.Float()
    becquerel = fields.Float()
