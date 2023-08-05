grid-control options
====================

.. _global:
global options
--------------

* ``cmdargs`` = <list of values> (Default: '')
    Automatically added command line arguments

* ``config id`` = <text> (Default: <config file name w/o extension> or 'unnamed')
    Identifier for the current configuration

* ``delete`` = <job selector> (Default: '')
    The unfinished jobs selected by this expression are cancelled

* ``gui`` = <plugin> (Default: 'BasicConsoleGUI')
    Specify GUI plugin to handle the user interaction

    List of available plugins:
     * ANSIGUI_ (alias: ansi)
     * BasicConsoleGUI_ (alias: console)
     * CPWebserver_ (alias: cherrypy)

* ``include`` = <list of values> (Default: '')
    List of additional config files which provide default values. These config files are processed in addition to the files: /etc/grid-control.conf, ~/.grid-control.conf and <GCDIR>/default.conf

* ``include override`` = <list of values> (Default: '')
    List of additional config files which will override anything in the current config file.

* ``package paths`` = <list of paths> (Default: '')
    Specify paths to additional grid-control packages with user defined plugins that are outside of the base package directory

* ``plugin paths`` = <list of paths> (Default: '<current directory>')
    Specifies paths that are used to search for plugins

* ``reset`` = <job selector> (Default: '')
    The jobs selected by this expression are reset to the INIT state

* ``variable markers`` = <list of values> (Default: '@ __')
    Specifies how variables are marked

* ``workdir`` = <path> (Default: <workdir base>/work.<config file name>)
    Location of the grid-control work directory. Usually based on the name of the config file

* ``workdir base`` = <path> (Default: <config file path>)
    Directory where the default workdir is created

* ``workdir create`` = <boolean> (Default: True)
    Skip interactive question about workdir creation

* ``workdir space`` = <integer> (Default: 10)
    Lower space limit in the work directory. Monitoring can be deactived with 0

* ``workflow`` = <plugin[:name]> (Default: 'Workflow:global')
    Specifies the workflow that is being run

    List of available plugins:
     * Workflow


.. _Workflow:
Workflow options
----------------

* ``backend`` = <list of plugin[:name] ...>
    Select the backend to use for job submission

    List of available plugins:
     * CreamWMS_ (alias: cream)
     * EuropeanDataGrid_ (alias: EDG, LCG)
     * GliteWMS_ (alias: gwms)
     * GridEngine_ (alias: SGE, UGE, OGE)
     * Host_ (alias: Localhost)
     * InactiveWMS_ (alias: inactive)

* ``backend manager`` = <plugin> (Default: 'MultiWMS')
    Specify compositor class to merge the different plugins given in ``backend``

    List of available compositor plugins:
     * MultiWMS_

* ``task / module`` = <plugin[:name]>
    Select the task module to run

    List of available plugins:
     * CMSSWAdvanced_ (alias: CMSSW_Advanced)
     * CMSSW_
     * ROOTTask_ (alias: ROOTMod, root)
     * UserTask_ (alias: UserMod, user, script)

* ``action`` = <list of values> (Default: 'check retrieve submit')
    Specify the actions and the order in which grid-control should perform them

* ``continuous`` = <boolean> (Default: False)
    Enable continuous running mode

* ``duration`` = <duration hh[:mm[:ss]]> (Default: <continuous mode on: infinite (-1), off: exit immediately (0)>)
    Maximal duration of the job processing pass. The default depends on the value of the 'continuous' option.

* ``event handler manager`` = <plugin> (Default: 'CompatEventHandlerManager')
    Specify event handler plugin to manage dual event handlers (that are both remote and local)

    List of available plugins:
     * CompatEventHandlerManager_ (alias: compat)

* ``job manager`` = <plugin[:name]> (Default: 'SimpleJobManager')
    Specify the job management plugin to handle the job cycle

    List of available plugins:
     * SimpleJobManager_ (alias: default)

* ``submission`` = <boolean> (Default: True)
    Toggle to control the submission of jobs

* ``submission time requirement`` = <duration hh[:mm[:ss]]> (Default: <wall time>)
    Toggle to control the submission of jobs

* ``workdir space timeout`` = <duration hh[:mm[:ss]]> (Default: 00:00:05)
    Specify timeout for workdir space check


.. _SimpleJobManager:
SimpleJobManager options
------------------------

* ``abort report`` = <plugin[:name]> (Default: 'LocationReport')
    Specify report plugin to display in case of job cancellations

    List of available plugins:
     * ANSIHeaderReport_ (alias: ansiheader)
     * ANSIReport_ (alias: ansireport)
     * ANSITheme_ (alias: ansi)
     * BackendReport_ (alias: backend)
     * BarReport_ (alias: bar)
     * BasicHeaderReport_ (alias: basicheader)
     * BasicReport_ (alias: basicreport)
     * BasicTheme_ (alias: basic)
     * ColorBarReport_ (alias: cbar)
     * LeanHeaderReport_ (alias: leanheader)
     * LeanReport_ (alias: leanreport)
     * LeanTheme_ (alias: lean)
     * LocationHistoryReport_ (alias: history)
     * LocationReport_ (alias: location)
     * MapReport_ (alias: map)
     * ModernReport_ (alias: modern)
     * ModuleReport_ (alias: module)
     * NullReport_ (alias: null)
     * PlotReport_ (alias: plot)
     * PluginReport_ (alias: plugin)
     * TimeReport_ (alias: time)
     * TrivialReport_ (alias: trivial)
     * VariablesReport_ (alias: variables, vars)

* ``chunks check`` = <integer> (Default: 100)
    Specify maximal number of jobs to check in each job cycle

* ``chunks enabled`` = <boolean> (Default: True)
    Toggle to control if only a chunk of jobs are processed each job cycle

* ``chunks retrieve`` = <integer> (Default: 100)
    Specify maximal number of jobs to retrieve in each job cycle

* ``chunks submit`` = <integer> (Default: 100)
    Specify maximal number of jobs to submit in each job cycle

* ``defect tries / kick offender`` = <integer> (Default: 10)
    Threshold for dropping jobs causing status retrieval errors (disable check with 0)

* ``in flight`` = <integer> (Default: no limit (-1))
    Maximum number of concurrently submitted jobs

* ``in queue`` = <integer> (Default: no limit (-1))
    Maximum number of queued jobs

* ``job database`` = <plugin> (Default: 'TextFileJobDB')
    Specify job database plugin that is used to store job information

    List of available plugins:
     * Migrate2ZippedJobDB_ (alias: migrate)
     * TextFileJobDB_ (alias: textdb)
     * ZippedJobDB_ (alias: zipdb)

* ``jobs`` = <integer> (Default: no limit (-1))
    Maximum number of jobs (truncated to task maximum)

* ``local event handler / local monitor`` = <list of plugin[:name] ...> (Default: 'logmonitor')
    Specify local event handler plugins to track the task / job progress on the submission host

    List of available plugins:
     * BasicLogEventHandler_ (alias: logmonitor)
     * DashboardLocal_ (alias: dashboard)
     * JabberAlarm_ (alias: jabber)
     * ScriptEventHandler_ (alias: scripts)

* ``local event handler manager`` = <plugin> (Default: 'MultiLocalEventHandler')
    Specify compositor class to merge the different plugins given in ``local event handler``

    List of available compositor plugins:
     * MultiLocalEventHandler_ (alias: multi)

* ``max retry`` = <integer> (Default: no limit (-1))
    Number of resubmission attempts for failed jobs

* ``output processor`` = <plugin> (Default: 'SandboxProcessor')
    Specify plugin that processes the output sandbox of successful jobs

    List of available plugins:
     * SandboxProcessor_ (alias: null)

* ``queue timeout`` = <duration hh[:mm[:ss]]> (Default: disabled (-1))
    Resubmit jobs after staying some time in initial state

* ``selected`` = <text> (Default: '')
    Apply general job selector

* ``shuffle`` = <boolean> (Default: False)
    Submit jobs in random order

* ``unknown timeout`` = <duration hh[:mm[:ss]]> (Default: disabled (-1))
    Cancel jobs without status information after staying in this state for the specified time

* ``verify chunks`` = <list of values> (Default: '-1')
    Specifies how many jobs to submit initially, and use to verify the workflow. If sufficient jobs succeed, all remaining jobs are enabled for submission

* ``verify threshold / verify reqs`` = <list of values> (Default: '0.5')
    Specifies the fraction of jobs in the verification chunk that must succeed


.. _backend:
backend options
---------------

* ``<prefix> chunk interval`` = <integer> (Default: <depends on the process>)
    Specify the interval between (submit, check, ...) chunks

* ``<prefix> chunk size`` = <integer> (Default: <depends on the process>)
    Specify the size of (submit, check, ...) chunks

* ``access token / proxy`` = <list of plugin[:name] ...> (Default: 'TrivialAccessToken')
    Specify access token plugins that are necessary for job submission

    List of available plugins:
     * AFSAccessToken_ (alias: afs, AFSProxy, KerberosAccessToken)
     * ARCAccessToken_ (alias: arc, arcproxy)
     * TrivialAccessToken_ (alias: trivial, TrivialProxy)
     * VomsAccessToken_ (alias: voms, VomsProxy)

* ``access token manager`` = <plugin> (Default: 'MultiAccessToken')
    Specify compositor class to merge the different plugins given in ``access token``

    List of available compositor plugins:
     * MultiAccessToken_ (alias: multi)

* ``cancel timeout`` = <duration hh[:mm[:ss]]> (Default: 00:01:00)
    Specify timeout of the process that is used to cancel jobs

* ``sb input manager`` = <plugin[:name]> (Default: 'LocalSBStorageManager')
    Specify transfer manager plugin to transfer sandbox input files

    List of available plugins:
     * StorageManager

* ``se input manager`` = <plugin[:name]> (Default: 'SEStorageManager')
    Specify transfer manager plugin to transfer SE input files

    List of available plugins:
     * StorageManager

* ``se output manager`` = <plugin[:name]> (Default: 'SEStorageManager')
    Specify transfer manager plugin to transfer SE output files

    List of available plugins:
     * StorageManager


.. _UserTask:
UserTask options
----------------

* ``wall time`` = <duration hh[:mm[:ss]]>
    Requested wall time also used for checking the proxy lifetime

* ``cpu time`` = <duration hh[:mm[:ss]]> (Default: <wall time>)
    Requested cpu time

* ``cpus / cores`` = <integer> (Default: 1)
    Requested number of cpus per node

* ``datasource names`` = <list of values> (Default: 'dataset')
    Specify list of data sources that will be created for use in the parameter space definition

* ``depends`` = <list of values> (Default: '')
    List of environment setup scripts that the jobs depend on

* ``gzip output`` = <boolean> (Default: True)
    Toggle the compression of the job log files for stdout and stderr

* ``input files`` = <list of paths> (Default: '')
    List of files that should be transferred to the landing zone of the job on the worker node. Only for small files - send large files via SE!

* ``internal parameter factory`` = <plugin> (Default: 'BasicParameterFactory')
    Specify the parameter factory plugin that is used to generate the basic grid-control parameters

    List of available plugins:
     * BasicParameterFactory_ (alias: basic)
     * ModularParameterFactory_ (alias: modular)
     * SimpleParameterFactory_ (alias: simple)

* ``job name generator`` = <plugin> (Default: 'DefaultJobName')
    Specify the job name plugin that generates the job name that is given to the backend

    List of available plugins:
     * ConfigurableJobName_ (alias: config)
     * DefaultJobName_ (alias: default)

* ``landing zone space left`` = <integer> (Default: 1)
    Minimum amount of disk space (in MB) that the job has to leave in the landing zone directory while running

* ``landing zone space used`` = <integer> (Default: 100)
    Maximum amount of disk space (in MB) that the job is allowed to use in the landing zone directory while running

* ``memory`` = <integer> (Default: unspecified (-1))
    Requested memory in MB. Some batch farms have very low default memory limits in which case it is necessary to specify this option!

* ``node timeout`` = <duration hh[:mm[:ss]]> (Default: disabled (-1))
    Cancel job after some time on worker node

* ``output files`` = <list of values> (Default: '')
    List of files that should be transferred to the job output directory on the submission machine. Only for small files - send large files via SE!

* ``parameter adapter`` = <plugin> (Default: 'TrackedParameterAdapter')
    Specify the parameter adapter plugin that translates parameter point to job number

    List of available plugins:
     * BasicParameterAdapter_ (alias: basic)
     * TrackedParameterAdapter_ (alias: tracked)

* ``scratch space left`` = <integer> (Default: 1)
    Minimum amount of disk space (in MB) that the job has to leave in the scratch directory while running. If the landing zone itself is the scratch space, the scratch thresholds apply

* ``scratch space used`` = <integer> (Default: 5000)
    Maximum amount of disk space (in MB) that the job is allowed to use in the scratch directory while running. If the landing zone itself is the scratch space, the scratch thresholds apply

* ``se min size`` = <integer> (Default: -1)
    TODO: DELETE

* ``subst files`` = <list of values> (Default: '')
    List of files that will be subjected to variable substituion

* ``task date`` = <text> (Default: <current date: YYYY-MM-DD>)
    Persistent date when the task was started

* ``task id`` = <text> (Default: 'GCxxxxxxxxxxxx')
    Persistent task identifier that is generated at the start of the task

* ``task name generator`` = <plugin> (Default: 'DefaultTaskName')
    Specify the task name plugin that generates the task name that is given to the backend

    List of available plugins:
     * DefaultTaskName_ (alias: default)

* ``task time`` = <text> (Default: <current time: HHMMSS>)
    Persistent time when the task was started


.. _CMSSW:
CMSSW options
-------------

* ``wall time`` = <duration hh[:mm[:ss]]>
    Requested wall time also used for checking the proxy lifetime

* ``area files`` = <filter option> (Default: '-.* -config bin lib python module data *.xml *.sql *.db *.cfi *.cff *.py -CVS -work.* *.pcm')
    List of files that should be taken from the CMSSW project area for running the job

* ``area files matcher`` = <plugin> (Default: 'BlackWhiteMatcher')
    Specify matcher plugin that is used to match filter expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``area files basename`` = <boolean> (Default: True)
    Toggle between using the relative path or just the file base name to match area files

* ``arguments`` = <text> (Default: '')
    Arguments that will be passed to the *cmsRun* call

* ``config file`` = <list of paths> (Default: <no default> or '' if prolog / epilog script is given)
    List of config files that will be sequentially processed by *cmsRun* calls

* ``cpu time`` = <duration hh[:mm[:ss]]> (Default: <wall time>)
    Requested cpu time

* ``cpus / cores`` = <integer> (Default: 1)
    Requested number of cpus per node

* ``datasource names`` = <list of values> (Default: 'dataset')
    Specify list of data sources that will be created for use in the parameter space definition

* ``depends`` = <list of values> (Default: '')
    List of environment setup scripts that the jobs depend on

* ``events per job`` = <text> (Default: '0')
    This sets the variable MAX_EVENTS if no datasets are present

* ``gzip output`` = <boolean> (Default: True)
    Toggle the compression of the job log files for stdout and stderr

* ``input files`` = <list of paths> (Default: '')
    List of files that should be transferred to the landing zone of the job on the worker node. Only for small files - send large files via SE!

* ``instrumentation`` = <boolean> (Default: True)
    Toggle to control the instrumentation of CMSSW config files for running over data / initializing the RNG for MC production

* ``instrumentation fragment`` = <path> (Default: <grid-control cms package>/share/fragmentForCMSSW.py)
    Path to the instrumentation fragment that is appended to the CMSSW config file if instrumentation is enabled

* ``internal parameter factory`` = <plugin> (Default: 'BasicParameterFactory')
    Specify the parameter factory plugin that is used to generate the basic grid-control parameters

    List of available plugins:
     * BasicParameterFactory_ (alias: basic)
     * ModularParameterFactory_ (alias: modular)
     * SimpleParameterFactory_ (alias: simple)

* ``job name generator`` = <plugin> (Default: 'DefaultJobName')
    Specify the job name plugin that generates the job name that is given to the backend

    List of available plugins:
     * ConfigurableJobName_ (alias: config)
     * DefaultJobName_ (alias: default)

* ``landing zone space left`` = <integer> (Default: 1)
    Minimum amount of disk space (in MB) that the job has to leave in the landing zone directory while running

* ``landing zone space used`` = <integer> (Default: 100)
    Maximum amount of disk space (in MB) that the job is allowed to use in the landing zone directory while running

* ``memory`` = <integer> (Default: unspecified (-1))
    Requested memory in MB. Some batch farms have very low default memory limits in which case it is necessary to specify this option!

* ``node timeout`` = <duration hh[:mm[:ss]]> (Default: disabled (-1))
    Cancel job after some time on worker node

* ``output files`` = <list of values> (Default: '')
    List of files that should be transferred to the job output directory on the submission machine. Only for small files - send large files via SE!

* ``parameter adapter`` = <plugin> (Default: 'TrackedParameterAdapter')
    Specify the parameter adapter plugin that translates parameter point to job number

    List of available plugins:
     * BasicParameterAdapter_ (alias: basic)
     * TrackedParameterAdapter_ (alias: tracked)

* ``project area`` = <path> (Default: <depends on ``scram arch`` and ``scram project``>)
    Specify location of the CMSSW project area that should be send with the job. Instead of the CMSSW project area, it is possible to specify ``scram arch`` and ``scram project`` to use a fresh CMSSW project

* ``scram arch`` = <text> (Default: <depends on ``project area``>)
    Specify scram architecture that should be used by the job (eg. 'slc7_amd64_gcc777'). When using an existing CMSSW project area with ``project area``, this option uses the default value taken from the project area

* ``scram arch requirements`` = <boolean> (Default: True)
    Toggle the inclusion of the scram architecture in the job requirements

* ``scram project`` = <list of values> (Default: '')
    Specify scram project that should be used by the job (eg. 'CMSSW CMSSW_9_9_9')

* ``scram project requirements`` = <boolean> (Default: False)
    Toggle the inclusion of the scram project name in the job requirements

* ``scram project version requirements`` = <boolean> (Default: False)
    Toggle the inclusion of the scram project version in the job requirements

* ``scram version`` = <text> (Default: 'scramv1')
    Specify scram version that should be used by the job

* ``scratch space left`` = <integer> (Default: 1)
    Minimum amount of disk space (in MB) that the job has to leave in the scratch directory while running. If the landing zone itself is the scratch space, the scratch thresholds apply

* ``scratch space used`` = <integer> (Default: 5000)
    Maximum amount of disk space (in MB) that the job is allowed to use in the scratch directory while running. If the landing zone itself is the scratch space, the scratch thresholds apply

* ``se min size`` = <integer> (Default: -1)
    TODO: DELETE

* ``se project area / se runtime`` = <boolean> (Default: True)
    Toggle to specify how the CMSSW project area should be transferred to the worker node

* ``subst files`` = <list of values> (Default: '')
    List of files that will be subjected to variable substituion

* ``task date`` = <text> (Default: <current date: YYYY-MM-DD>)
    Persistent date when the task was started

* ``task id`` = <text> (Default: 'GCxxxxxxxxxxxx')
    Persistent task identifier that is generated at the start of the task

* ``task name generator`` = <plugin> (Default: 'DefaultTaskName')
    Specify the task name plugin that generates the task name that is given to the backend

    List of available plugins:
     * DefaultTaskName_ (alias: default)

* ``task time`` = <text> (Default: <current time: HHMMSS>)
    Persistent time when the task was started

* ``vo software dir / cmssw dir`` = <text> (Default: '')
    This option allows to override of the VO_CMS_SW_DIR environment variable


.. _CMSSWAdvanced:
CMSSWAdvanced options
---------------------

* ``wall time`` = <duration hh[:mm[:ss]]>
    Requested wall time also used for checking the proxy lifetime

* ``area files`` = <filter option> (Default: '-.* -config bin lib python module data *.xml *.sql *.db *.cfi *.cff *.py -CVS -work.* *.pcm')
    List of files that should be taken from the CMSSW project area for running the job

* ``area files matcher`` = <plugin> (Default: 'BlackWhiteMatcher')
    Specify matcher plugin that is used to match filter expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``area files basename`` = <boolean> (Default: True)
    Toggle between using the relative path or just the file base name to match area files

* ``arguments`` = <text> (Default: '')
    Arguments that will be passed to the *cmsRun* call

* ``config file`` = <list of paths> (Default: <no default> or '' if prolog / epilog script is given)
    List of config files that will be sequentially processed by *cmsRun* calls

* ``cpu time`` = <duration hh[:mm[:ss]]> (Default: <wall time>)
    Requested cpu time

* ``cpus / cores`` = <integer> (Default: 1)
    Requested number of cpus per node

* ``datasource names`` = <list of values> (Default: 'dataset')
    Specify list of data sources that will be created for use in the parameter space definition

* ``depends`` = <list of values> (Default: '')
    List of environment setup scripts that the jobs depend on

* ``events per job`` = <text> (Default: '0')
    This sets the variable MAX_EVENTS if no datasets are present

* ``gzip output`` = <boolean> (Default: True)
    Toggle the compression of the job log files for stdout and stderr

* ``input files`` = <list of paths> (Default: '')
    List of files that should be transferred to the landing zone of the job on the worker node. Only for small files - send large files via SE!

* ``instrumentation`` = <boolean> (Default: True)
    Toggle to control the instrumentation of CMSSW config files for running over data / initializing the RNG for MC production

* ``instrumentation fragment`` = <path> (Default: <grid-control cms package>/share/fragmentForCMSSW.py)
    Path to the instrumentation fragment that is appended to the CMSSW config file if instrumentation is enabled

* ``internal parameter factory`` = <plugin> (Default: 'BasicParameterFactory')
    Specify the parameter factory plugin that is used to generate the basic grid-control parameters

    List of available plugins:
     * BasicParameterFactory_ (alias: basic)
     * ModularParameterFactory_ (alias: modular)
     * SimpleParameterFactory_ (alias: simple)

* ``job name generator`` = <plugin> (Default: 'DefaultJobName')
    Specify the job name plugin that generates the job name that is given to the backend

    List of available plugins:
     * ConfigurableJobName_ (alias: config)
     * DefaultJobName_ (alias: default)

* ``landing zone space left`` = <integer> (Default: 1)
    Minimum amount of disk space (in MB) that the job has to leave in the landing zone directory while running

* ``landing zone space used`` = <integer> (Default: 100)
    Maximum amount of disk space (in MB) that the job is allowed to use in the landing zone directory while running

* ``memory`` = <integer> (Default: unspecified (-1))
    Requested memory in MB. Some batch farms have very low default memory limits in which case it is necessary to specify this option!

* ``nickname config`` = <lookup specifier> (Default: '')
    Allows to specify a dictionary with list of config files that will be sequentially processed by *cmsRun* calls. The dictionary key is the job dependent dataset nickname

* ``nickname config matcher`` = <plugin> (Default: 'RegExMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``nickname constants`` = <list of values> (Default: '')
    Allows to specify a list of nickname dependent variables. The value of the variables is specified separately in the form of a dictionary. (This option is deprecated, since *all* variables support this functionality now!)

* ``nickname lumi filter`` = <dictionary> (Default: '')
    Allows to specify a dictionary with nickname dependent lumi filter expressions. (This option is deprecated, since the normal option ``lumi filter`` already supports this!)

* ``node timeout`` = <duration hh[:mm[:ss]]> (Default: disabled (-1))
    Cancel job after some time on worker node

* ``output files`` = <list of values> (Default: '')
    List of files that should be transferred to the job output directory on the submission machine. Only for small files - send large files via SE!

* ``parameter adapter`` = <plugin> (Default: 'TrackedParameterAdapter')
    Specify the parameter adapter plugin that translates parameter point to job number

    List of available plugins:
     * BasicParameterAdapter_ (alias: basic)
     * TrackedParameterAdapter_ (alias: tracked)

* ``project area`` = <path> (Default: <depends on ``scram arch`` and ``scram project``>)
    Specify location of the CMSSW project area that should be send with the job. Instead of the CMSSW project area, it is possible to specify ``scram arch`` and ``scram project`` to use a fresh CMSSW project

* ``scram arch`` = <text> (Default: <depends on ``project area``>)
    Specify scram architecture that should be used by the job (eg. 'slc7_amd64_gcc777'). When using an existing CMSSW project area with ``project area``, this option uses the default value taken from the project area

* ``scram arch requirements`` = <boolean> (Default: True)
    Toggle the inclusion of the scram architecture in the job requirements

* ``scram project`` = <list of values> (Default: '')
    Specify scram project that should be used by the job (eg. 'CMSSW CMSSW_9_9_9')

* ``scram project requirements`` = <boolean> (Default: False)
    Toggle the inclusion of the scram project name in the job requirements

* ``scram project version requirements`` = <boolean> (Default: False)
    Toggle the inclusion of the scram project version in the job requirements

* ``scram version`` = <text> (Default: 'scramv1')
    Specify scram version that should be used by the job

* ``scratch space left`` = <integer> (Default: 1)
    Minimum amount of disk space (in MB) that the job has to leave in the scratch directory while running. If the landing zone itself is the scratch space, the scratch thresholds apply

* ``scratch space used`` = <integer> (Default: 5000)
    Maximum amount of disk space (in MB) that the job is allowed to use in the scratch directory while running. If the landing zone itself is the scratch space, the scratch thresholds apply

* ``se min size`` = <integer> (Default: -1)
    TODO: DELETE

* ``se project area / se runtime`` = <boolean> (Default: True)
    Toggle to specify how the CMSSW project area should be transferred to the worker node

* ``subst files`` = <list of values> (Default: '')
    List of files that will be subjected to variable substituion

* ``task date`` = <text> (Default: <current date: YYYY-MM-DD>)
    Persistent date when the task was started

* ``task id`` = <text> (Default: 'GCxxxxxxxxxxxx')
    Persistent task identifier that is generated at the start of the task

* ``task name generator`` = <plugin> (Default: 'DefaultTaskName')
    Specify the task name plugin that generates the task name that is given to the backend

    List of available plugins:
     * DefaultTaskName_ (alias: default)

* ``task time`` = <text> (Default: <current time: HHMMSS>)
    Persistent time when the task was started

* ``vo software dir / cmssw dir`` = <text> (Default: '')
    This option allows to override of the VO_CMS_SW_DIR environment variable


.. _dataset:
dataset options
---------------

* ``<datasource>`` = <list of [<nickname> : [<provider> :]] <dataset specifier> > (Default: '')
    Specify list of datasets to process (including optional nickname and dataset provider information)

    List of available plugins:
     * ConfigDataProvider_ (alias: config)
     * DASProvider_ (alias: das)
     * DBS2Provider_ (alias: dbs2)
     * DBS3Provider_ (alias: dbs3, dbs)
     * DBSInfoProvider_ (alias: dbsinfo)
     * FileProvider_ (alias: file)
     * GCProvider_ (alias: gc)
     * ListProvider_ (alias: list)
     * ScanProvider_ (alias: scan)

* ``<datasource> manager`` = <plugin> (Default: ':ThreadedMultiDatasetProvider:')
    Specify compositor class to merge the different plugins given in ``<datasource>``

    List of available compositor plugins:
     * MultiDatasetProvider_ (alias: multi)
     * ThreadedMultiDatasetProvider_ (alias: threaded)

* ``<datasource> default query interval`` = <duration hh[:mm[:ss]]> (Default: 00:01:00)
    Specify the default limit for the dataset query interval

* ``<datasource> nickname source / nickname source`` = <plugin> (Default: 'SimpleNickNameProducer')
    Specify nickname plugin that determines the nickname for datasets

    List of available plugins:
     * EmptyDataProcessor_ (alias: empty)
     * EntriesConsistencyDataProcessor_ (alias: consistency)
     * EntriesCountDataProcessor_ (alias: events, EventsCountDataProcessor)
     * InlineNickNameProducer_ (alias: inline)
     * LocationDataProcessor_ (alias: location)
     * LumiDataProcessor_ (alias: lumi)
     * NickNameConsistencyProcessor_ (alias: nickconsistency)
     * NullDataProcessor_ (alias: null)
     * PartitionEstimator_ (alias: estimate, SplitSettingEstimator)
     * SimpleNickNameProducer_ (alias: simple)
     * SimpleStatsDataProcessor_ (alias: stats)
     * SortingDataProcessor_ (alias: sort)
     * URLCountDataProcessor_ (alias: files, FileCountDataProcessor)
     * URLDataProcessor_ (alias: ignore, FileDataProcessor)
     * UniqueDataProcessor_ (alias: unique)

* ``<datasource> partition processor / partition processor`` = <list of plugins> (Default: 'TFCPartitionProcessor LocationPartitionProcessor MetaPartitionProcessor BasicPartitionProcessor')
    Specify list of plugins that process partitions

    List of available plugins:
     * BasicPartitionProcessor_ (alias: basic)
     * CMSSWPartitionProcessor_ (alias: cmsswpart)
     * LFNPartitionProcessor_ (alias: lfnprefix)
     * LocationPartitionProcessor_ (alias: location)
     * LumiPartitionProcessor_ (alias: lumi)
     * MetaPartitionProcessor_ (alias: metadata)
     * RequirementsPartitionProcessor_ (alias: reqs)
     * TFCPartitionProcessor_ (alias: tfc)

* ``<datasource> partition processor manager`` = <plugin> (Default: 'MultiPartitionProcessor')
    Specify compositor class to merge the different plugins given in ``<datasource> partition processor``

    List of available compositor plugins:
     * MultiPartitionProcessor_ (alias: multi)

* ``<datasource> processor`` = <list of plugins> (Default: 'NickNameConsistencyProcessor EntriesConsistencyDataProcessor URLDataProcessor URLCountDataProcessor EntriesCountDataProcessor EmptyDataProcessor UniqueDataProcessor LocationDataProcessor')
    Specify list of plugins that process datasets before the partitioning

    List of available plugins:
     * EmptyDataProcessor_ (alias: empty)
     * EntriesConsistencyDataProcessor_ (alias: consistency)
     * EntriesCountDataProcessor_ (alias: events, EventsCountDataProcessor)
     * InlineNickNameProducer_ (alias: inline)
     * LocationDataProcessor_ (alias: location)
     * LumiDataProcessor_ (alias: lumi)
     * NickNameConsistencyProcessor_ (alias: nickconsistency)
     * NullDataProcessor_ (alias: null)
     * PartitionEstimator_ (alias: estimate, SplitSettingEstimator)
     * SimpleNickNameProducer_ (alias: simple)
     * SimpleStatsDataProcessor_ (alias: stats)
     * SortingDataProcessor_ (alias: sort)
     * URLCountDataProcessor_ (alias: files, FileCountDataProcessor)
     * URLDataProcessor_ (alias: ignore, FileDataProcessor)
     * UniqueDataProcessor_ (alias: unique)

* ``<datasource> processor manager`` = <plugin> (Default: 'MultiDataProcessor')
    Specify compositor class to merge the different plugins given in ``<datasource> processor``

    List of available compositor plugins:
     * MultiDataProcessor_ (alias: multi)

* ``<datasource> provider / default provider`` = <text> (Default: 'ListProvider')
    Specify the name of the default dataset provider

* ``<datasource> refresh`` = <duration hh[:mm[:ss]]> (Default: disabled (-1))
    Specify the interval to check for changes in the used datasets

* ``<datasource> splitter`` = <plugin> (Default: 'FileBoundarySplitter')
    Specify the dataset splitter plugin to partition the dataset

* ``resync jobs`` = <enum: APPEND|PRESERVE|FILLGAP|REORDER> (Default: APPEND)
    Specify how resynced jobs should be handled

* ``resync metadata`` = <list of values> (Default: '')
    List of metadata keys that have configuration options to specify how metadata changes are handled by a dataset resync

* ``resync mode <metadata key>`` = <enum: DISABLE|COMPLETE|IGNORE> (Default: COMPLETE)
    Specify how changes in the given metadata key affect partitions during resync

* ``resync mode added`` = <enum: COMPLETE|IGNORE> (Default: COMPLETE)
    Sets the resync mode for new files

* ``resync mode expand`` = <enum: DISABLE|COMPLETE|CHANGED|IGNORE> (Default: CHANGED)
    Sets the resync mode for expanded files

* ``resync mode removed`` = <enum: DISABLE|COMPLETE|IGNORE> (Default: COMPLETE)
    Sets the resync mode for removed files

* ``resync mode shrink`` = <enum: DISABLE|COMPLETE|CHANGED|IGNORE> (Default: CHANGED)
    Sets the resync mode for shrunken files


.. _CMS grid proxy:
CMS grid proxy options
----------------------

* ``new proxy lifetime`` = <duration hh[:mm[:ss]]> (Default: 03:12:00)
    Specify the new lifetime for a newly created grid proxy

* ``new proxy roles`` = <list of values> (Default: '')
    Specify the new roles for a newly created grid proxy (in addition to the cms role)

* ``new proxy timeout`` = <duration hh[:mm[:ss]]> (Default: 00:00:10)
    Specify the timeout for waiting to create a new grid proxy


.. _TaskExecutableWrapper:
TaskExecutableWrapper options
-----------------------------

* ``[<prefix>] arguments`` = <text> (Default: '')
    Specify arguments for the executable

* ``[<prefix>] executable`` = <text> (Default: <no default> or '')
    Path to the executable

* ``[<prefix>] send executable`` = <boolean> (Default: True)
    Toggle to control if the specified executable should be send together with the job


.. __get_lookup_args:
_get_lookup_args options
------------------------

* ``<parameter>`` = <text>
    Specify the output variable name where the lookup result is stored

* ``default lookup`` = <text>
    Specify the default lookup variable

* ``<parameter> empty set`` = <boolean> (Default: False)
    Toggle if empty lookup results should be interpreted as an empty set [] or alternatively as an empty string ''

* ``<parameter> matcher`` = <text> (Default: <default matcher given by 'default matcher'>)
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``default matcher`` = <text> (Default: 'equal')
    Specify the default matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)


.. _interactive:
interactive options
-------------------

* ``<option name>`` = <boolean> (Default: True)
    Toggle to switch interactive questions on and off

* ``dataset name assignment`` = <boolean> (Default: True)
    Toggle interactive question about issues with the bijectivity of the dataset / block name assignments in the scan provider

* ``delete jobs`` = <boolean> (Default: True)
    Toggle interactivity of job deletion requests

* ``reset jobs`` = <boolean> (Default: True)
    Toggle interactivity of job reset requests


.. _logging:
logging options
---------------

* ``<logger name> file`` = <text>
    Log file used by file logger

* ``<logger name> <handler> code context / <logger name> code context`` = <integer> (Default: 2)
    Number of code context lines in shown exception logs

* ``<logger name> <handler> detail lower limit / <logger name> detail lower limit`` = <enum: LEVEL 0..50|NOTSET|DEBUG3...DEBUG|INFO3..INFO|DEFAULT|WARNING|ERROR|CRITICAL> (Default: DEBUG)
    Logging messages below this log level will use the long form output

* ``<logger name> <handler> detail upper limit / <logger name> detail upper limit`` = <enum: LEVEL 0..50|NOTSET|DEBUG3...DEBUG|INFO3..INFO|DEFAULT|WARNING|ERROR|CRITICAL> (Default: ERROR)
    Logging messages above this log level will use the long form output

* ``<logger name> <handler> file stack / <logger name> file stack`` = <integer> (Default: 1)
    Level of detail for file stack information shown in exception logs

* ``<logger name> <handler> thread stack / <logger name> thread stack`` = <integer> (Default: 1)
    Level of detail for thread stack information shown in exception logs

* ``<logger name> <handler> tree / <logger name> tree`` = <integer> (Default: 2)
    Level of detail for exception tree information shown in exception logs

* ``<logger name> <handler> variables / <logger name> variables`` = <integer> (Default: 200)
    Level of detail for variable information shown in exception logs

* ``<logger name> debug file`` = <list of paths> (Default: '"<gc dir>/debug.log" "/tmp/gc.debug.<uid>.<pid>" "~/gc.debug"')
    Logfile used by debug file logger. In case multiple paths are specified, the first usable path will be used

* ``<logger name> handler`` = <list of values> (Default: '')
    List of log handlers

* ``<logger name> level`` = <enum: LEVEL 0..50|NOTSET|DEBUG3...DEBUG|INFO3..INFO|DEFAULT|WARNING|ERROR|CRITICAL> (Default: <depends on the logger>)
    Logging level of log handlers

* ``<logger name> propagate`` = <boolean> (Default: <depends on the logger>)
    Toggle log propagation

* ``activity stream stderr / activity stream`` = <plugin> (Default: 'DefaultActivityMonitor')
    Specify activity stream class that displays the current activity tree on stderr

    List of available plugins:
     * DefaultActivityMonitor_ (alias: default_stream)
     * NullOutputStream_ (alias: null)
     * SingleActivityMonitor_ (alias: single_stream)
     * TimedActivityMonitor_ (alias: timed_stream)

* ``activity stream stdout / activity stream`` = <plugin> (Default: 'DefaultActivityMonitor')
    Specify activity stream class that displays the current activity tree on stdout

    List of available plugins:
     * DefaultActivityMonitor_ (alias: default_stream)
     * NullOutputStream_ (alias: null)
     * SingleActivityMonitor_ (alias: single_stream)
     * TimedActivityMonitor_ (alias: timed_stream)

* ``debug mode`` = <boolean> (Default: False)
    Toggle debug mode (detailed exception output on stdout)

* ``display logger`` = <boolean> (Default: False)
    Toggle display of logging structure


.. _parameters:
parameters options
------------------

* ``<parameter expression>`` = <text> (Default: '')
    Specify parameter value

* ``<parameter expression> key delimeter`` = <text> (Default: ',')
    Specify delimeter to split parameter names

* ``<parameter expression> parse dict`` = <boolean> (Default: True)
    Toggle parsing parameter value as dictionary when it contains '=>'

* ``<parameter expression> type`` = <text> (Default: 'default')
    Specify parameter tuple parser

    List of available parameter tuple parser plugins:
     * BinningTupleParser_ (alias: binning)
     * DefaultTupleParser_ (alias: tuple, default)

* ``<parameter>`` = <text> (Default: '')
    Specify parameter value

* ``<parameter> repeat`` = <text> (Default: '1')
    Specify how often the parameter values should be repeated

* ``<parameter> repeat idx <index>`` = <text> (Default: '1')
    Specify how often the given parameter value should be repeated

* ``<parameter> type`` = <text> (Default: 'default')
    Specify parameter value parser

    List of available parameter value parser plugins:
     * ExprParameterParser_ (alias: expr, eval)
     * FormatParameterParser_ (alias: format)
     * GitParameterParser_ (alias: git)
     * LinesParameterParser_ (alias: lines)
     * RegexTransformParameterParser_ (alias: regex_transform)
     * ShellParameterParser_ (alias: shell, default)
     * SplitParameterParser_ (alias: split)
     * SvnParameterParser_ (alias: svn)
     * TransformParameterParser_ (alias: transform)
     * VerbatimParameterParser_ (alias: verbatim)

* ``parameters`` = <text> (Default: '')
    Specify the parameter expression that defines the parameter space. The syntax depends on the used parameter factory


.. _ActivityMonitor:
ActivityMonitor options
-----------------------

* ``activity max length`` = <integer> (Default: 75)
    Specify maximum number of activities to display


.. _Matcher:
Matcher options
---------------

* ``<prefix> case sensitive`` = <boolean> (Default: True)
    Toggle case sensitivity for the matcher


.. _MultiActivityMonitor:
MultiActivityMonitor options
----------------------------

* ``activity fold fraction`` = <float> (Default: 0.5)
    Start folding activities when the number of activities reach this fraction of the display height

* ``activity max length`` = <integer> (Default: 75)
    Specify maximum number of activities to display


.. _TimedActivityMonitor:
TimedActivityMonitor options
----------------------------

* ``activity interval`` = <float> (Default: 5.0)
    Specify interval to display the

* ``activity max length`` = <integer> (Default: 75)
    Specify maximum number of activities to display


.. _GridEngineDiscoverNodes:
GridEngineDiscoverNodes options
-------------------------------

* ``discovery timeout`` = <duration hh[:mm[:ss]]> (Default: 00:00:30)
    Specify timeout of the process that is used to discover backend featues


.. _GridEngineDiscoverQueues:
GridEngineDiscoverQueues options
--------------------------------

* ``discovery timeout`` = <duration hh[:mm[:ss]]> (Default: 00:00:30)
    Specify timeout of the process that is used to discover backend featues


.. _PBSDiscoverNodes:
PBSDiscoverNodes options
------------------------

* ``discovery timeout`` = <duration hh[:mm[:ss]]> (Default: 00:00:30)
    Specify timeout of the process that is used to discover backend featues


.. _CheckJobsWithProcess:
CheckJobsWithProcess options
----------------------------

* ``check promiscuous`` = <boolean> (Default: False)
    Toggle the indiscriminate logging of the job status tool output

* ``check timeout`` = <duration hh[:mm[:ss]]> (Default: 00:01:00)
    Specify timeout of the process that is used to check the job status


.. _GridEngineCheckJobs:
GridEngineCheckJobs options
---------------------------

* ``check promiscuous`` = <boolean> (Default: False)
    Toggle the indiscriminate logging of the job status tool output

* ``check timeout`` = <duration hh[:mm[:ss]]> (Default: 00:01:00)
    Specify timeout of the process that is used to check the job status

* ``job status key`` = <list of values> (Default: 'JB_jobnum JB_jobnumber JB_job_number')
    List of property names that are used to determine the wms id of jobs


.. _EmptyDataProcessor:
EmptyDataProcessor options
--------------------------

* ``<datasource> remove empty blocks`` = <boolean> (Default: True)
    Toggle removal of empty blocks (without files) from the dataset

* ``<datasource> remove empty files`` = <boolean> (Default: True)
    Toggle removal of empty files (without entries) from the dataset


.. _EntriesCountDataProcessor:
EntriesCountDataProcessor options
---------------------------------

* ``<datasource> limit entries / <datasource> limit events`` = <integer> (Default: -1)
    Specify the number of events after which addition files in the dataset are discarded


.. _LocationDataProcessor:
LocationDataProcessor options
-----------------------------

* ``<datasource> location filter`` = <filter option> (Default: '')
    Specify dataset location filter. Dataset without locations have the filter whitelist applied

* ``<datasource> location filter plugin`` = <plugin> (Default: 'StrictListFilter')
    Specify plugin that is used to filter the list

    List of available filters:
     * MediumListFilter_ (alias: try_strict)
     * StrictListFilter_ (alias: strict, require)
     * WeakListFilter_ (alias: weak, prefer)

* ``<datasource> location filter matcher`` = <plugin> (Default: 'BlackWhiteMatcher')
    Specify matcher plugin that is used to match filter expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``<datasource> location filter order`` = <enum: SOURCE|MATCHER> (Default: SOURCE)
    Specify the order of the filtered list


.. _LumiDataProcessor:
LumiDataProcessor options
-------------------------

* ``<datasource> lumi filter / lumi filter`` = <lookup specifier> (Default: '')
    Specify lumi filter for the dataset (as nickname dependent dictionary)

* ``<datasource> lumi filter matcher`` = <plugin> (Default: 'StartMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``<datasource> lumi filter strictness / lumi filter strictness`` = <enum: STRICT|WEAK> (Default: STRICT)
    Specify if the lumi filter requires the run and lumi information (strict) or just the run information (weak)

* ``<datasource> lumi keep / lumi keep`` = <enum: RUNLUMI|RUN|NONE> (Default: <Run/none depending on active/inactive lumi filter>)
    Specify which lumi metadata to retain


.. _MultiDataProcessor:
MultiDataProcessor options
--------------------------

* ``<datasource> processor prune`` = <boolean> (Default: True)
    Toggle the removal of unused dataset processors from the dataset processing pipeline


.. _PartitionEstimator:
PartitionEstimator options
--------------------------

* ``<datasource> target partitions / target partitions`` = <integer> (Default: -1)
    Specify the number of partitions the splitter should aim for

* ``<datasource> target partitions per nickname / target partitions per nickname`` = <integer> (Default: -1)
    Specify the number of partitions per nickname the splitter should aim for


.. _SortingDataProcessor:
SortingDataProcessor options
----------------------------

* ``<datasource> block sort`` = <boolean> (Default: False)
    Toggle sorting of dataset blocks

* ``<datasource> files sort`` = <boolean> (Default: False)
    Toggle sorting of dataset files

* ``<datasource> location sort`` = <boolean> (Default: False)
    Toggle sorting of dataset locations

* ``<datasource> sort`` = <boolean> (Default: False)
    Toggle sorting of datasets


.. _URLCountDataProcessor:
URLCountDataProcessor options
-----------------------------

* ``<datasource> limit urls / <datasource> limit files`` = <integer> (Default: -1)
    Specify the number of files after which addition files in the dataset are discarded

* ``<datasource> limit urls fraction / <datasource> limit files fraction`` = <float> (Default: -1.0)
    Specify the fraction of files in the dataset that should be used


.. _URLDataProcessor:
URLDataProcessor options
------------------------

* ``<datasource> ignore urls / <datasource> ignore files`` = <filter option> (Default: '')
    Specify list of url / data sources to remove from the dataset

* ``<datasource> ignore urls plugin`` = <plugin> (Default: 'WeakListFilter')
    Specify plugin that is used to filter the list

    List of available filters:
     * MediumListFilter_ (alias: try_strict)
     * StrictListFilter_ (alias: strict, require)
     * WeakListFilter_ (alias: weak, prefer)

* ``<datasource> ignore urls matcher`` = <plugin> (Default: 'BlackWhiteMatcher')
    Specify matcher plugin that is used to match filter expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``<datasource> ignore urls order`` = <enum: SOURCE|MATCHER> (Default: SOURCE)
    Specify the order of the filtered list


.. _EntriesConsistencyDataProcessor:
EntriesConsistencyDataProcessor options
---------------------------------------

* ``<datasource> check entry consistency`` = <enum: WARN|ABORT|IGNORE> (Default: ABORT)
    Toggle check for consistency between the number of events given in the block and and the files


.. _NickNameConsistencyProcessor:
NickNameConsistencyProcessor options
------------------------------------

* ``<datasource> check nickname collision`` = <enum: WARN|ABORT|IGNORE> (Default: ABORT)
    Toggle nickname collision checks between datasets

* ``<datasource> check nickname consistency`` = <enum: WARN|ABORT|IGNORE> (Default: ABORT)
    Toggle check for consistency of nicknames between blocks in the same dataset


.. _UniqueDataProcessor:
UniqueDataProcessor options
---------------------------

* ``<datasource> check unique block`` = <enum: WARN|ABORT|SKIP|IGNORE|RECORD> (Default: ABORT)
    Specify how to react to duplicated dataset and blockname combinations

* ``<datasource> check unique url`` = <enum: WARN|ABORT|SKIP|IGNORE|RECORD> (Default: ABORT)
    Specify how to react to duplicated urls in the dataset


.. _InlineNickNameProducer:
InlineNickNameProducer options
------------------------------

* ``<datasource> nickname expr / nickname expr`` = <text> (Default: 'current_nickname')
    Specify a python expression (using the variables dataset, block and oldnick) to generate the dataset nickname for the block


.. _SimpleNickNameProducer:
SimpleNickNameProducer options
------------------------------

* ``<datasource> nickname full name / nickname full name`` = <boolean> (Default: True)
    Toggle if the nickname should be constructed from the complete dataset name or from the first part


.. _CMSBaseProvider:
CMSBaseProvider options
-----------------------

* ``<datasource> lumi filter / lumi filter`` = <lookup specifier> (Default: '')
    Specify lumi filter for the dataset (as nickname dependent dictionary)

* ``<datasource> lumi filter matcher`` = <plugin> (Default: 'StartMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``<datasource> lumi metadata / lumi metadata`` = <boolean> (Default: <True/False for active/inactive lumi filter>)
    Toggle the retrieval of lumi metadata

* ``allow phedex`` = <boolean> (Default: True)
    Allow phedex queries to retrieve dataset location information

* ``dbs instance`` = <text> (Default: 'prod/global')
    Specify the default dbs instance (by url or instance identifier) to use for dataset queries

* ``location format`` = <enum: HOSTNAME|SITEDB|BOTH> (Default: HOSTNAME)
    Specify the format of the DBS location information

* ``only complete sites`` = <boolean> (Default: True)
    Toggle the inclusion of incomplete sites in the dataset location information

* ``only valid`` = <boolean> (Default: True)
    Toggle the inclusion of files marked as invalid dataset

* ``phedex sites`` = <filter option> (Default: '-* T1_*_Disk T2_* T3_*')
    Toggle the inclusion of files marked as invalid dataset

* ``phedex sites plugin`` = <plugin> (Default: 'StrictListFilter')
    Specify plugin that is used to filter the list

    List of available filters:
     * MediumListFilter_ (alias: try_strict)
     * StrictListFilter_ (alias: strict, require)
     * WeakListFilter_ (alias: weak, prefer)

* ``phedex sites matcher`` = <plugin> (Default: 'BlackWhiteMatcher')
    Specify matcher plugin that is used to match filter expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``phedex sites order`` = <enum: SOURCE|MATCHER> (Default: SOURCE)
    Specify the order of the filtered list


.. _ConfigDataProvider:
ConfigDataProvider options
--------------------------

* ``<dataset URL>`` = <int> [<metadata in JSON format>]
    The option name corresponds to the URL of the dataset file. The value consists of the number of entry and some optional file metadata

* ``events`` = <integer> (Default: automatic (-1))
    Specify total number of events in the dataset

* ``metadata`` = <text> (Default: '[]')
    List of metadata keys in the dataset

* ``metadata common`` = <text> (Default: '[]')
    Specify metadata values in JSON format that are common to all files in the dataset

* ``nickname`` = <text> (Default: <determined by dataset expression>)
    Specify the dataset nickname

* ``prefix`` = <text> (Default: '')
    Specify the common prefix of URLs in the dataset

* ``se list`` = <text> (Default: '')
    Specify list of locations where the dataset is available


.. _ScanProviderBase:
ScanProviderBase options
------------------------

* ``<prefix> guard override`` = <list of values> (Default: <taken from the selected info scanners>)
    Override the list of guard keys that are preventing files from being in the same datasets or block

* ``<prefix> hash keys`` = <list of values> (Default: '')
    Specify list of keys that are used to determine the datasets or block assigment of files

* ``<prefix> key select`` = <list of values> (Default: '')
    Specify list of dataset or block hashes that are selected for this data source

* ``<prefix> name pattern`` = <text> (Default: '')
    Specify the name pattern for the dataset or block (using variables that are common to all files in the dataset or block)

* ``scanner`` = <list of values> (Default: <depends on other configuration options>)
    Specify list of info scanner plugins to retrieve dataset informations


.. _DASProvider:
DASProvider options
-------------------

* ``<datasource> lumi filter / lumi filter`` = <lookup specifier> (Default: '')
    Specify lumi filter for the dataset (as nickname dependent dictionary)

* ``<datasource> lumi filter matcher`` = <plugin> (Default: 'StartMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``<datasource> lumi metadata / lumi metadata`` = <boolean> (Default: <True/False for active/inactive lumi filter>)
    Toggle the retrieval of lumi metadata

* ``allow phedex`` = <boolean> (Default: True)
    Allow phedex queries to retrieve dataset location information

* ``das instance`` = <text> (Default: 'https://cmsweb.cern.ch/das/cache')
    Specify url to the DAS instance that is used to query the datasets

* ``dbs instance`` = <text> (Default: 'prod/global')
    Specify the default dbs instance (by url or instance identifier) to use for dataset queries

* ``location format`` = <enum: HOSTNAME|SITEDB|BOTH> (Default: HOSTNAME)
    Specify the format of the DBS location information

* ``only complete sites`` = <boolean> (Default: True)
    Toggle the inclusion of incomplete sites in the dataset location information

* ``only valid`` = <boolean> (Default: True)
    Toggle the inclusion of files marked as invalid dataset

* ``phedex sites`` = <filter option> (Default: '-* T1_*_Disk T2_* T3_*')
    Toggle the inclusion of files marked as invalid dataset

* ``phedex sites plugin`` = <plugin> (Default: 'StrictListFilter')
    Specify plugin that is used to filter the list

    List of available filters:
     * MediumListFilter_ (alias: try_strict)
     * StrictListFilter_ (alias: strict, require)
     * WeakListFilter_ (alias: weak, prefer)

* ``phedex sites matcher`` = <plugin> (Default: 'BlackWhiteMatcher')
    Specify matcher plugin that is used to match filter expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)

* ``phedex sites order`` = <enum: SOURCE|MATCHER> (Default: SOURCE)
    Specify the order of the filtered list


.. _ThreadedMultiDatasetProvider:
ThreadedMultiDatasetProvider options
------------------------------------

* ``dataprovider thread max`` = <integer> (Default: 3)
    Specify the maximum number of threads used for dataset query

* ``dataprovider thread timeout`` = <duration hh[:mm[:ss]]> (Default: 00:15:00)
    Specify the timeout for the dataset query to fail


.. _DBSInfoProvider:
DBSInfoProvider options
-----------------------

* ``<prefix> guard override`` = <list of values> (Default: <taken from the selected info scanners>)
    Override the list of guard keys that are preventing files from being in the same datasets or block

* ``<prefix> hash keys`` = <list of values> (Default: '')
    Specify list of keys that are used to determine the datasets or block assigment of files

* ``<prefix> key select`` = <list of values> (Default: '')
    Specify list of dataset or block hashes that are selected for this data source

* ``<prefix> name pattern`` = <text> (Default: '')
    Specify the name pattern for the dataset or block (using variables that are common to all files in the dataset or block)

* ``discovery`` = <boolean> (Default: False)
    Toggle discovery only mode (without DBS consistency checks)

* ``scanner`` = <list of values> (Default: <depends on other configuration options>)
    Specify list of info scanner plugins to retrieve dataset informations


.. _EventBoundarySplitter:
EventBoundarySplitter options
-----------------------------

* ``<datasource> entries per job / <datasource> events per job / entries per job / events per job`` = <lookup specifier>
    Set granularity of dataset splitter

* ``<datasource> entries per job matcher`` = <plugin> (Default: 'StartMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)


.. _FLSplitStacker:
FLSplitStacker options
----------------------

* ``<datasource> splitter stack / splitter stack`` = <list of plugins> (Default: 'BlockBoundarySplitter')
    Specify sequence of dataset splitters. All dataset splitters except for the last one have to be of type 'FileLevelSplitter', splitting only along file boundaries


.. _FileBoundarySplitter:
FileBoundarySplitter options
----------------------------

* ``<datasource> files per job / files per job`` = <lookup specifier>
    Set granularity of dataset splitter

* ``<datasource> files per job matcher`` = <plugin> (Default: 'StartMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)


.. _HybridSplitter:
HybridSplitter options
----------------------

* ``<datasource> entries per job / <datasource> events per job / entries per job / events per job`` = <lookup specifier>
    Set guideline for the granularity of the dataset splitter

* ``<datasource> entries per job matcher`` = <plugin> (Default: 'StartMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)


.. _RunSplitter:
RunSplitter options
-------------------

* ``<datasource> run range / run range`` = <lookup specifier> (Default: {None: 1})
    Specify number of sequential runs that are processed per job

* ``<datasource> run range matcher`` = <plugin> (Default: 'StartMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)


.. _UserMetadataSplitter:
UserMetadataSplitter options
----------------------------

* ``split metadata`` = <lookup specifier> (Default: '')
    Specify the name of the metadata variable that is used to partition the dataset into equivalence classes

* ``split metadata matcher`` = <plugin> (Default: 'StartMatcher')
    Specify matcher plugin that is used to match the lookup expressions

    List of available matcher plugins:
     * AlwaysMatcher_ (alias: always)
     * BlackWhiteMatcher_ (alias: blackwhite)
     * EndMatcher_ (alias: end)
     * EqualMatcher_ (alias: equal)
     * ExprMatcher_ (alias: expr, eval)
     * RegExMatcher_ (alias: regex)
     * ShellStyleMatcher_ (alias: shell)
     * StartMatcher_ (alias: start)


.. _CompatEventHandlerManager:
CompatEventHandlerManager options
---------------------------------

* ``event handler / monitor`` = <list of values> (Default: 'scripts')
    Specify list of dual event handlers


.. _ANSIGUI:
ANSIGUI options
---------------

* ``gui element`` = <list of plugin[:name] ...> (Default: 'report activity log')
    Specify the GUI elements that form the GUI display

    List of available plugins:
     * ActivityGUIElement_ (alias: activity)
     * ReportGUIElement_ (alias: report)
     * SpanGUIElement_ (alias: span)
     * UserLogGUIElement_ (alias: log)

* ``gui element manager`` = <plugin> (Default: 'MultiGUIElement')
    Specify compositor class to merge the different plugins given in ``gui element``

    List of available compositor plugins:
     * MultiGUIElement_ (alias: multi)

* ``gui redraw delay`` = <float> (Default: 0.05)
    Specify the redraw delay for gui elements

* ``gui redraw interval`` = <float> (Default: 0.1)
    Specify the redraw interval for gui elements


.. _BasicConsoleGUI:
BasicConsoleGUI options
-----------------------

* ``report`` = <list of plugin[:name] ...> (Default: 'BasicTheme')
    Type of report to display during operations

    List of available plugins:
     * ANSIHeaderReport_ (alias: ansiheader)
     * ANSIReport_ (alias: ansireport)
     * ANSITheme_ (alias: ansi)
     * BackendReport_ (alias: backend)
     * BarReport_ (alias: bar)
     * BasicHeaderReport_ (alias: basicheader)
     * BasicReport_ (alias: basicreport)
     * BasicTheme_ (alias: basic)
     * ColorBarReport_ (alias: cbar)
     * LeanHeaderReport_ (alias: leanheader)
     * LeanReport_ (alias: leanreport)
     * LeanTheme_ (alias: lean)
     * LocationHistoryReport_ (alias: history)
     * LocationReport_ (alias: location)
     * MapReport_ (alias: map)
     * ModernReport_ (alias: modern)
     * ModuleReport_ (alias: module)
     * NullReport_ (alias: null)
     * PlotReport_ (alias: plot)
     * PluginReport_ (alias: plugin)
     * TimeReport_ (alias: time)
     * TrivialReport_ (alias: trivial)
     * VariablesReport_ (alias: variables, vars)

* ``report manager`` = <plugin> (Default: 'MultiReport')
    Specify compositor class to merge the different plugins given in ``report``

    List of available compositor plugins:
     * MultiReport_ (alias: multi)


.. _CPWebserver:
CPWebserver options
-------------------

* ``hide login`` = <boolean> (Default: False)
{
  "after_user": "", 
  "api": "get_bool", 
  "api_text": "Allows to specify a boolean value with true/false, 1/0, yes/no, ...", 
  "append_options": [], 
  "args": [], 
  "available_filter_list": " * MediumListFilter_ (alias: try_strict)\n * StrictListFilter_ (alias: strict, require)\n * WeakListFilter_ (alias: weak, prefer)\n", 
  "available_matcher_list": " * AlwaysMatcher_ (alias: always)\n * BlackWhiteMatcher_ (alias: blackwhite)\n * EndMatcher_ (alias: end)\n * EqualMatcher_ (alias: equal)\n * ExprMatcher_ (alias: expr, eval)\n * RegExMatcher_ (alias: regex)\n * ShellStyleMatcher_ (alias: shell)\n * StartMatcher_ (alias: start)\n", 
  "available_parameter_parser": " * ExprParameterParser_ (alias: expr, eval)\n * FormatParameterParser_ (alias: format)\n * GitParameterParser_ (alias: git)\n * LinesParameterParser_ (alias: lines)\n * RegexTransformParameterParser_ (alias: regex_transform)\n * ShellParameterParser_ (alias: shell, default)\n * SplitParameterParser_ (alias: split)\n * SvnParameterParser_ (alias: svn)\n * TransformParameterParser_ (alias: transform)\n * VerbatimParameterParser_ (alias: verbatim)\n", 
  "available_parameter_tuple_parser": " * BinningTupleParser_ (alias: binning)\n * DefaultTupleParser_ (alias: tuple, default)\n", 
  "bases": [
    "object", 
    "Plugin", 
    "ConfigurablePlugin", 
    "GUI"
  ], 
  "callers": [
    "CPWebserver"
  ], 
  "default": false, 
  "default_raw": false, 
  "fn": "../../packages/grid_control_gui/gui_cherrypy.py", 
  "format": "'True' or 'False'", 
  "fqfn": "config.get_bool", 
  "kwargs": {}, 
  "line": "\t\tself._hide_login = config.get_bool('hide login', False, on_change=None)\n", 
  "lineno": 114, 
  "location": "CPWebserver", 
  "on_change": null, 
  "on_valid": "<no validation>", 
  "option": "hide login", 
  "option_display": "hide login", 
  "option_map": {
    "<call:output_vn.lstrip('!')>": "<parameter>", 
    "<call:self._get_varexpr(<name:vn>)>": "<parameter expression>", 
    "<call:self._get_varexpr(<parameter>)>": "<parameter expression>", 
    "<name:broker_prefix>": "<broker prefix>", 
    "<name:datasource_name>": "<datasource>", 
    "<name:handler_name>": "<handler>", 
    "<name:idx>": "<index>", 
    "<name:logger_name>": "<logger name>", 
    "<name:option_prefix>": "<prefix>", 
    "<name:output_vn>": "<parameter>", 
    "<name:prefix>": "<prefix>", 
    "<name:ref_name>": "<parameter reference>", 
    "<name:storage_channel>": "<storage channel>", 
    "<name:storage_type>": "<storage type>", 
    "<name:varexpr>": "<parameter expression>", 
    "<name:vn>": "<parameter>"
  }, 
  "options": [
    "hide login"
  ], 
  "output_altopt": "", 
  "output_default": "(Default: False)", 
  "pargs": "<impossible>", 
  "persistent": false, 
  "prepend_options": [], 
  "raw_args": [
    "'hide login'", 
    false
  ], 
  "raw_kwargs": {}, 
  "scope": "config", 
  "short": "<boolean>", 
  "user_text": ""
}
