def power_used_during_work_interval(work_interval, power_rate):
    """
    Helper function for compute_total_power_consumption()
    Computes the power consumed during the current work interval

    Inputs:
    work_interval: list<int>
    Contains the begin and end time of the current work interval

    Outputs:
    The power consumed during the work interval
    """
    # Everything is in minutes, don't need to worry about unit conversions
    begin_time = work_interval[0]
    end_time = work_interval[1]
    work_interval = end_time - begin_time
    return work_interval * power_rate


def power_used_during_break_interval(curr_begin_time, prev_end_time,
                                     time_from_norm_2_ss, time_from_ss_2_sleep,
                                     normal_mode_power_use,
                                     screen_saver_mode_power_use,
                                     sleep_mode_power_use):
    """
    Helper function for compute_total_power_consumption()
    Computes the total power consumption during a break interval

    Inputs:
    curr_begin_time : <int>
    The begin time, in minutes, of the current work interval

    prev_end_time : <int>
    The end time, in minutes, of the previous work interval

    time_from_norm_2_ss : <float>
    Contains time, in minutes, laptop must be left alone in order to enter
    screen-saver mode

    time_from_ss_2_sleep : <float>
    time, in minutes, laptop must be left alone in screen-saver mode order to
    enter sleep mode

    normal_mode_power_use : <float>
    ate of power consumption, in watts/min, of the laptop when in
    normal mode

    screen_saver_mode_power_use : <float>
    Rate of power consumption, in watts/min, of the laptop when in
    screen-saver mode

    sleep_mode_power_use : <float>
    Rate of power consumption, in watts/min, of the laptop when in
    sleep mode

    Outputs:
    The power consumed during the break interval
    """
    # Calculate difference between start of current work interval and
    # end of last work interval
    break_interval = curr_begin_time - prev_end_time

    # Calculate time required to enter sleep mode from normal mode
    time_from_norm_2_sleep = time_from_norm_2_ss + time_from_ss_2_sleep

    # Calculate and return power consumption when the break interval is
    # strictly less than the time required to enter screen saver mode
    if break_interval < time_from_norm_2_ss:
        return break_interval * normal_mode_power_use

    # Calculate and return power consumption when the break interval is
    # greater than or equal to the time required to enter screen saver mode,
    # but strictly less than the time required to enter sleep mode
    elif time_from_norm_2_ss <= break_interval < time_from_norm_2_sleep:

        # Calculate duration for which laptop is in sleep mode
        time_in_ss_mode = break_interval - time_from_norm_2_sleep

        return time_from_norm_2_ss * normal_mode_power_use + \
               time_in_ss_mode * screen_saver_mode_power_use

    # Calculate and return power consumption when the break interval is
    # greater than the time required for the laptop to go from normal mode to
    # sleep mode
    else:

        # Calculate laptop's time in sleep mode
        time_in_sleep_mode = break_interval - time_from_norm_2_sleep

        return time_from_norm_2_ss * normal_mode_power_use + \
               time_from_ss_2_sleep * screen_saver_mode_power_use + \
               time_in_sleep_mode * sleep_mode_power_use


def compute_total_power_consumption(n_lines_and_computer_behavior_data):
    """
    A. Power Consumption Calculation Tom is interested in the power
    consumption of his favourite laptop. His laptop has three modes. In
    normal mode, the laptop consumes P_1 watts per minute. T_1 minutes after
    Tom has last moved the mouse or touched the keyboard, a screen-saver
    starts, and the power consumption changes to P_2 watts per minute.
    Finally, after T_2 minutes from the start of the screen-saver, the laptop
    switches to "sleep" mode, and consumes P_3 watts per minute. If Tom moves
    the mouse or touches the keyboard when the laptop is in the second or
    third mode, it switches to the first (normal) mode. Tom's work with the
    laptop can be divided into n time periods [l_1, r_1], [l_2, r_2], ...,
     [l_n, r_n]. During each interval Tom continuously moves the mouse and
    presses buttons on the keyboard. Between the periods Tom stays away from
    the laptop. Find out the total amount of power consumed by the laptop
    during the period [l_1, r_n].

    Input The first line contains 6 integer numbers n, P_1, P_2, P_3, T_1,
    T_2 (1 ≤ n ≤ 100, 0 ≤ P_1, P_2, P_3 ≤ 100, 1 ≤ T_1, T_2 ≤ 60). The following
    n lines contain description of Tom's work. Each i-th of these lines
    contains two space-separated integers:
        l_i and r_i (0 ≤ l_i < r_i ≤ 1440, r_i < l (# i + 1 for i < n),
    which stand for the start and the end of the i-th period of work.

    Output:
    total_power_consumption: <float>
    Print the total power consumption of the laptop.
    """
    # During work intervals:
    # Laptop will consume power at a rate of P_1.
    # Can simply multiply duration of work interval (r_i - l_i) by the normal
    # power consumption, P_1, to get total power consumption during work
    # intervals.

    # For time between work intervals:
    # Need to create a 2-element list that will contain the previous end time
    # and the current begin time. The difference between these two times
    # represents Tom's time away from the laptop. If difference is
    # greater than or equal to T_1, then laptop enters screen-saver mode and
    # consumes power at rate P_2. If time away is greater than T_1 + T_2,
    # then laptop is able to enter sleep-mode and consumes power at a rate
    # of P_3.
    # Power Used = max(difference - T1, 0)*P_1 +
    # (difference - T1, difference - (T1 + T2))*P_2 +
    # max(difference - (T1 + T2), 0)*P_3

    # Process inputs
    # first input is a single-lined string containing 6 parameters that are
    # space-separated:
    # 1) n : number of lines of work behavior
    # 2) P_1 : laptop power consumption in normal mode
    # 3) P_2 : laptop power consumption (watts/min) in screen-saver mode
    # 4) P_3 : laptop power consumption (watts/min) in sleep-mode
    # 5) T_1 : time, in minutes, laptop must be left alone in order to enter
    #          screen-saver mode
    # 6) T_2 : time, in minutes, laptop must be left alon after entering
    #          screen-saver mode to enter sleep-mode

    # Split line into separate elements (indicated by a single space),
    # store into a list and convert elements to floats
    global prev_end_time
    n_lines_and_computer_behavior_list = \
        list(map(float, num_lines_and_computer_behavior_data.split(" ")))
    n_lines = n_lines_and_computer_behavior_list[0]
    normal_mode_power_use = n_lines_and_computer_behavior_list[1]
    screen_saver_mode_power_use = n_lines_and_computer_behavior_list[2]
    sleep_mode_power_use = n_lines_and_computer_behavior_list[3]
    time_from_norm_2_screen_saver = n_lines_and_computer_behavior_list[4]
    time_from_ss_2_sleep = n_lines_and_computer_behavior_list[5]

    # Create lists that will contain the power consumption for each work
    # interval and each break interval
    power_use_during_work = []
    power_use_during_breaks = []

    # Next n lines are single-lined strings containing two parameters that
    # are space-separated (will require a while loop)
    # 1) l_i : begin time (in minutes) of working on laptop
    # 2) r_i : end time (in minutes) of working on laptop
    num_work_intervals = 0
    while num_work_intervals < n_lines:
        work_interval_str = input()
        # Split line into separate elements (indicated by a single space),
        # store into a list and convert elements to ints
        work_interval = list(map(int, work_interval_str.split(" ")))

        # Get power consumed during work interval
        work_power_use = power_used_during_work_interval(work_interval,
                                                         normal_mode_power_use)
        power_use_during_work.append(work_power_use)

        # Calculate break interval for work intervals after the first
        if num_work_intervals > 0:
            break_power_use = \
                power_used_during_break_interval(work_interval[0],
                                                 prev_end_time,
                                                 time_from_norm_2_screen_saver,
                                                 time_from_ss_2_sleep,
                                                 normal_mode_power_use,
                                                 screen_saver_mode_power_use,
                                                 sleep_mode_power_use)

            power_use_during_breaks.append(break_power_use)

            # Update end time for last work interval
        prev_end_time = work_interval[1]

        num_work_intervals += 1

    print(int(sum(power_use_during_work) + sum(power_use_during_breaks)))


if __name__ == "__main__":
    num_lines_and_computer_behavior_data = input()
    compute_total_power_consumption(num_lines_and_computer_behavior_data)

    # Examples
    # inputCopy
    # 1 3 2 1 5 10
    # 0 10
    # outputCopy
    # 30
    # inputCopy
    # 2 8 4 2 5 10
    # 20 30
    # 50 100
    # outputCopy
    # 570