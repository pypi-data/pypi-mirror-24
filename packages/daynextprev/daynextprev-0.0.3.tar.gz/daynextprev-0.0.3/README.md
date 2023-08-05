# day-nextprev


## Installation

    $ pip install daynextprev

## Usage


### Calc next day


    from daynextprev import next_day
    ny, nm, nd = next_day(2015, 2, 22)


### Calc previous day


    from daynextprev import prev_day
    py, pm, pd = prev_day(2017, 3, 1)


### Check leapyear

    from daynextprev import is_leapyear
    is_leapyear(2016)  # => True


### Calc last day of month


    from daynextprev import days_of_month
    days_of_month(2016, 2)  # => 29
