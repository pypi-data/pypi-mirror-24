
   ...    *    .   _  .
*  .  *     .   * (_)   *
  .      |*  ..   *   ..
   .  * \|  *  ___  . . *
*   \/   |/ \/{o,o}     .
  _\_\   |  / /)  )* _/_ *
      \ \| /,--"-"---  ..
_-----`  |(,__,__/__/_ .
       \ ||      ..
        ||| .            *
        |||
        |||
  , -=-~' .-^- _

Hoottit is a command line tool that can stream Reddit data (submissions
and comments) to a MongoDB database of choice. All it needs is two Reddit app
keys (in praw.ini) and a MongoDB URI set in the HOOT_MONGODBURI env variable.
If the database URI is not set, it automatically tries to connect
to localhost:27017. Since this application is best used as a long running
script, an optional HOOT_SENTRYDSN env variable can be set to capture any
warnings and errors that might appear (usually caused by problems with the
connection, but not only). The keepalive script can be used to keep the
application alive after it crashes. For more information about using the
application, type hoottit --help.
