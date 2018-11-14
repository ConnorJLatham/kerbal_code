import krpc
import time

# connecting to the server
conn = krpc.connect(name = 'Peanut Mk.1 Nov1318')
vessel = conn.space_center.active_vessel
print('Connected!')
print('Waiting 5 seconds')
time.sleep(5)

# Launching the vessel
print('Raising Throttle to Max')
vessel.control.throttle = 1
time.sleep(1)
print('Launching')
vessel.control.activate_next_stage()

# Monitor fuel use
fuel_amount = conn.get_call(vessel.resources.amount,'SolidFuel')
fuel_condition = conn.krpc.Expression.less_than(
    conn.krpc.Expression.call(fuel_amount),
    conn.krpc.Expression.constant_float(.1)
)
empty_event = conn.krpc.add_event(fuel_condition)
with empty_event.condition:
    empty_event.wait()
print('Shutting down throttle, fuel empty')
