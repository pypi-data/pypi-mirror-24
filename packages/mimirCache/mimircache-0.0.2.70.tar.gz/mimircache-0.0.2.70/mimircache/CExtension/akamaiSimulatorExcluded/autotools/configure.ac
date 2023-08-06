#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT(akamaiSimulator, 0.01, peter.waynechina@gmail.com)
AC_CONFIG_SRCDIR([cacheLayer.cpp])
AC_CONFIG_HEADERS([config.h])
AM_INIT_AUTOMAKE(akamaiSimulator, 0.0.1.0)

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC
AC_PROG_CPP

# Checks for libraries.
# FIXME: Replace `main' with a function in `-lm':
AC_CHECK_LIB([m], [main])

# Checks for header files.
AC_CHECK_HEADERS([stdlib.h string.h sys/time.h syslog.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_CHECK_HEADER_STDBOOL
AC_C_INLINE
AC_TYPE_SIZE_T

# Checks for library functions.
AC_FUNC_MALLOC
AC_FUNC_MKTIME
AC_FUNC_REALLOC
AC_CHECK_FUNCS([gettimeofday strtol])

AC_CONFIG_FILES([makefile])
AC_OUTPUT
