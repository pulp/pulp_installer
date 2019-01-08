# If adding new functions to this file, note that you can add help text to the function
# by defining a variable with name _<function>_help containing the help text

SERVICES=("pulp_content_app pulp_worker@1 pulp_worker@2 pulp_resource_manager")

_paction() {
    echo systemctl $@ ${SERVICES}
    sudo systemctl $@ ${SERVICES}
}

pstart() {
    _paction start
}
_pstart_help="Start all pulp-related services"

pstop() {
    _paction stop
}
_pstop_help="Stop all pulp-related services"

prestart() {
    _paction restart
}
_prestart_help="Restart all pulp-related services"

pstatus() {
    _paction status
}
_pstatus_help="Report the status of all pulp-related services"

preset() {
    echo "Due to its similarity to 'prestart', 'preset' has been renamed to 'pclean'."
    echo "Please use 'pclean' instead, and remember to update any script that might be calling it."
    sleep 3
    pclean
}
# intentionally undocumented, only list pclean in help for this

pclean() {
    workon pulp
    pulp-manager reset_db --noinput
    pulp-manager migrate auth --noinput
    pulp-manager migrate
    pulp-manager reset-admin-password --password admin
}
_pclean_help="Restore pulp to a clean-installed state"
# can get away with not resetting terminal settings here since it gets reset in phelp
_pclean_help="$_pclean_help - `setterm -foreground red -bold on`THIS DESTROYS YOUR PULP DATA"

pjournal() {
    # build up the journalctl cmdline per-unit
    journal_cmd="journalctl"
    for svc in ${SERVICES}; do
        journal_cmd="$journal_cmd -u $svc"
    done

    if [ -z $1 ]; then
        # not passed any args, follow the units' journals by default
        $journal_cmd -f
    else
        # passed some args, send all args through to journalctl
        $journal_cmd $@
    fi
}
_pjournal_help="Interact with the journal for pulp-related units
    pjournal takes optional journalctl args e.g. 'pjournal -r', runs pjournal -f by default"

ptest() {
    # based on the test running in the travis conf yaml
    # travis should run the same tests devs do, but that gets a little tricky
    # with Django, tracked in https://pulp.plan.io/issues/2266
    # For now, this is a reasonable approximation until we figure out how to test pulp 3.
    workon pulp
    flake8 --config flake8.cfg app
    # manage.py test will create and migrate its own database,
    # but we still need to make the migrations for it to be able to do that.
    python manage.py makemigrations pulp_app
    # We have to be explicit if an app doesn't already have migrations
    python manage.py makemigrations pulp_file
    # Auth migrations must be run before pulpcore to generate schema that the User model relates to.
    python manage.py migrate auth --noinput
    python manage.py test pulpcore/
}
_ptest_help="Run tests for pulp and all installed plugins/services"

ptests() {
    ptest $@
}
# undocumented alias for backward compatibility

_ppopulate() {
	echo "I don't know how to populate anything yet!"
}
_ppopulate_help="Populate pulp with repositories"

pprocs() {
    print_procs() {
        # prints a header string with number of pids, list of pids, and a newline spacer
        # $1 is the header string, $2 is a newline-separated list of pids, see usage below
        echo "$1 ($(echo $2|wc -w)):"
        echo $2
        echo
    }

    # override IFS to prevent bash splitting pgrep output on newlines
    IFS=''
    print_procs "Pulp worker processes" `pgrep -f "pulpcore.tasking.celery_app -c 1"`
    print_procs "Pulp Resource Manager processes" `pgrep -f "pulpcore.tasking.celery_app -n resource_manager"`
    print_procs "Pulp WSGI processes:" `pgrep -f "wsgi:pulp"`
    unset IFS
}
_pprocs_help="Print running pulp processes IDs"

pdebug() {
    telnet 127.0.0.1 4444
}
_pdebug_help="Telnet to a debugger listening locally on port 4444"

phelp() {
    # get a list of declared functions, filter out ones with leading underscores as "private"
    funcs=$(declare -F | awk '{ print $3 }'| grep -v ^_)

    # for each func, if a help string is defined, assume it's a pulp function and print its help
    # (this is bash introspection via variable variables)
    for func in $funcs; do
        # get the "help" variable name for this function
        help_var="_${func}_help"
        # use ${!<varname>} syntax to eval the help_var
        help=${!help_var}
        # If the help var had a value, echo its value here (the value is function help text)
        if [ ! -z "$help" ]; then
            # make the function name easy to spot
            setterm -foreground yellow -bold on
            echo -n "$func"
            # reset terminal formatting before printing the help text
            # (implicitly format it as normal text)
            setterm -default
            echo ": $help"
        fi
    done

    # explicitly restore terminal formatting is reset before exiting function
    setterm -default
}
_phelp_help="Print this help"

alias phttp="http"
