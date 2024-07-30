# Start
- Initialize an array of X values at 0.

# Use a Stack Data Structure

## Processing Incoming Value
- Push incoming_val onto the stack.
- Increment incoming_val by its square (incoming_val += incoming_val^2).

## Removing the Last Value
- Decrease the current value by the square of the last value (current_val -= last_val^2).
- Pop the last value off the stack.

## Perform Calculation
- Divide the sum of the squared values by the number of values in the stack.
- Take the square root of the result to get the Root Mean Squared (RMS).

# Conclusion
- The process yields the Root Mean Squared (RMS) of the values.
