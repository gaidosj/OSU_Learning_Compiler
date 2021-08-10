function is_leap_year(year) {
    return year % 400 == 0 || year % 4 == 0 && year % 100 != 0;
}

if (is_leap_year(2021)) {
    print '2021 is a leap year!';
} else {
    print '2021 is not a leap year!';
}
