
#          Copyright Jamie Allsop 2015-2017
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

#-------------------------------------------------------------------------------
#   Quince
#-------------------------------------------------------------------------------

import os.path
import subprocess
import shlex
import platform
import glob

# Cuppa Imports
import cuppa.location
import cuppa.output_processor
from cuppa.log import logger



class QuinceException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)


class QuinceLibraryMethod(object):

    def __init__( self, location, src_path ):
        self._location = location
        self._src_path = src_path


    def __call__( self, env, linktype ):

        build_dir = os.path.join( self._location, env['build_dir'] )
        final_dir = os.path.normpath( os.path.join( build_dir, env['final_dir'] ) )

        env.BuildWith( 'boost' )

        objects = []
        for source in env.RecursiveGlob( "*.cpp", start=self._src_path, exclude_dirs=[ env['build_dir'] ] ):
            rel_path = os.path.relpath( str(source), self._location )
            obj_path = os.path.join( build_dir, os.path.splitext( rel_path )[0] ) + env['OBJSUFFIX']
            objects.append( env.Object( obj_path, source ) )

        if linktype == "static":
            return env.BuildStaticLib( "quince", objects, final_dir = final_dir )
        else:
            shared_lib = env.BuildSharedLib( "quince", objects, final_dir = final_dir )
            return env.Install( env['abs_final_dir'], shared_lib )



class build_with_quince(object):

    _name = "quince"
    _location = None

    @classmethod
    def add_options( cls, add_option ):
        location_name = cls._name + "-location"
        add_option( '--' + location_name, dest=location_name, type='string', nargs=1, action='store',
                    help = cls._name + ' location to build against' )


    @classmethod
    def add_to_env( cls, env, add_dependency  ):
        add_dependency( cls._name, cls.create )


    @classmethod
    def create( cls, env ):
        if not cls._location:
            location = env.get_option( cls._name + "-location" )
            if not location:
                logger.error( "Dependency not available - no location specified" )
                return None
            try:
                cls._location = cuppa.location.Location( env, location )
            except cuppa.location.LocationException as error:
                logger.error(
                    "Dependency not available - retrieving location failed with error [{}]."
                    .format( str(error) )
                )
                return None
        return build_with_quince( env )


    def __init__( self, env ):
        self._includes = [ os.path.join( self._location.local(), "include" ) ]
        self._src_path = os.path.join( self._location.local(), "src" )

        env.AddMethod( QuinceLibraryMethod( self._location.local(), self._src_path ), "QuinceLibrary" )


    def __call__( self, env, toolchain, variant ):

        env.AppendUnique( INCPATH = self._includes )

        env.AppendUnique( STATICLIBS = [
                env.QuinceLibrary( 'static' ),
                env.BoostStaticLibs( [
                        'filesystem',
                        'system',
                        'thread',
                ] ),
        ] )


    @classmethod
    def name( cls ):
        return cls._name

    def version( self ):
        return str(self._location.version())

    def repository( self ):
        return self._location.repository()

    def branch( self ):
        return self._location.branch()

    def revisions( self ):
        return self._location.revisions()



class QuincePostgresqlLibraryMethod(object):

    def __init__( self, location, src_path ):
        self._location = location
        self._src_path = src_path


    def __call__( self, env, linktype ):
        build_dir = os.path.join( self._location, env['build_dir'] )
        final_dir = os.path.normpath( os.path.join( build_dir, env['final_dir'] ) )

        env.BuildWith( 'boost' )

        objects = []
        for source in env.RecursiveGlob( "*.cpp", start=self._src_path, exclude_dirs=[ env['build_dir'] ] ):
            rel_path = os.path.relpath( str(source), self._location )
            obj_path = os.path.join( build_dir, os.path.splitext( rel_path )[0] ) +env['OBJSUFFIX']
            objects.append( env.Object( obj_path, source ) )

        if linktype == "static":
            return env.BuildStaticLib( "quince-postgresql", objects, final_dir = final_dir )
        else:
            shared_lib = env.BuildSharedLib( "quince-postgresql", objects, final_dir = final_dir )
            return env.Install( env['abs_final_dir'], shared_lib )



class quince_postgresql(object):

    _name = "quince-postgresql"
    _location = None

    @classmethod
    def add_options( cls, add_option ):

        location_name = cls._name + "-location"
        add_option( '--' + location_name, dest=location_name, type='string', nargs=1, action='store',
                    help = cls._name + ' location to build against' )

    @classmethod
    def add_to_env( cls, env, add_dependency  ):
        add_dependency( cls._name, cls.create )

    @classmethod
    def create( cls, env ):
        if not cls._location:
            location = env.get_option( cls._name + "-location" )
            if not location:
                logger.error( "postgresql: Dependency not available - no location specified" )
                return None
            try:
                cls._location = cuppa.location.Location( env, location )
            except cuppa.location.LocationException as error:
                logger.error(
                    "postgresql: Dependency not available - retrieving location failed with error [{}]."
                    .format( str(error) )
                )
                return None
        return quince_postgresql( env )


    def __init__( self, env ):
        self._flags = {}
        self._flags['INCPATH'] = [ os.path.join( self._location.local(), "include" ) ]

        pg_config = "pg_config"
        if platform.system() == "Windows":
            pg_config = pg_config + ".exe"
            if not cuppa.output_processor.command_available( pg_config ):
                # try to find the Postgresql install
                program_files = os.environ.get( "ProgramW6432" )
                postgresql_base = os.path.join( program_files, "PostgreSQL" )
                if os.path.exists( postgresql_base ):
                    paths = glob.glob( postgresql_base + '\\*' )
                    if len(paths):
                        paths.sort()
                        latest = paths[-1]
                        pg_config = '\"' + os.path.join( latest, "bin", pg_config ) + '\"'

        if cuppa.output_processor.command_available( pg_config ):
            command = "{pg_config} --includedir".format( pg_config = pg_config )
            libpq_include = subprocess.check_output( shlex.split( command ), stderr=subprocess.STDOUT ).strip()
            self._flags['INCPATH'].append( libpq_include )

            command = "{pg_config} --libdir".format( pg_config = pg_config )
            libpq_libpath = subprocess.check_output( shlex.split( command ), stderr=subprocess.STDOUT ).strip()
            self._flags['LIBPATH'] = [ libpq_libpath ]
        else:
            logger.error( "postgresql: pg_config not available so cannot determine LIBPATH for postgres libraries" )
            raise QuinceException( "pg_config not available" )

        self._flags['DYNAMICLIBS'] = [ 'pq' ]

        self._src_path = os.path.join( self._location.local(), "src" )

        env.AddMethod( QuincePostgresqlLibraryMethod( self._location.local(), self._src_path ), "QuincePostgresqlLibrary" )


    def __call__( self, env, toolchain, variant ):
        env.AppendUnique( INCPATH     = self._flags['INCPATH'] )
        env.AppendUnique( LIBPATH     = self._flags['LIBPATH'] )
        env.AppendUnique( DYNAMICLIBS = self._flags['DYNAMICLIBS'] )

        quince_postgresql_lib = env.QuincePostgresqlLibrary('static')
        quince_lib = env.QuinceLibrary('static')

        env.Append( STATICLIBS  = [
                quince_postgresql_lib,
                quince_lib,
                env.BoostStaticLibs( [ 'date_time' ] ),
        ] )


    @classmethod
    def name( cls ):
        return cls._name

    def version( self ):
        return str(self._location.version())

    def repository( self ):
        return self._location.repository()

    def branch( self ):
        return self._location.branch()

    def revisions( self ):
        return self._location.revisions()


class QuinceSqliteLibraryMethod(object):

    def __init__( self, location, src_path ):
        self._location = location
        self._src_path = src_path


    def __call__( self, env, linktype ):
        build_dir = os.path.join( self._location, env['build_dir'] )
        final_dir = os.path.normpath( os.path.join( build_dir, env['final_dir'] ) )

        env.BuildWith( 'boost' )

        objects = []
        for source in env.RecursiveGlob( "*.cpp", start=self._src_path, exclude_dirs=[ env['build_dir'] ] ):
            rel_path = os.path.relpath( str(source), self._location )
            obj_path = os.path.join( build_dir, os.path.splitext( rel_path )[0] ) +env['OBJSUFFIX']
            objects.append( env.Object( obj_path, source ) )

        if linktype == "static":
            return env.BuildStaticLib( "quince-sqlite", objects, final_dir = final_dir )
        else:
            shared_lib = env.BuildSharedLib( "quince-sqlite", objects, final_dir = final_dir )
            return env.Install( env['abs_final_dir'], shared_lib )


class quince_sqlite(object):

    _name = "quince-sqlite"
    _location = None

    @classmethod
    def add_options( cls, add_option ):

        location_name = cls._name + "-location"
        add_option( '--' + location_name, dest=location_name, type='string', nargs=1, action='store',
                    help = cls._name + ' location to build against' )

    @classmethod
    def add_to_env( cls, env, add_dependency  ):
        add_dependency( cls._name, cls.create )


    @classmethod
    def create( cls, env ):
        if not cls._location:
            location = env.get_option( cls._name + "-location" )
            if not location:
                logger.error( "sqlite: Dependency not available - no location specified" )
                return None
            try:
                cls._location = cuppa.location.Location( env, location )
            except cuppa.location.LocationException as error:
                logger.error(
                    "sqlite: Dependency not available - retrieving location failed with error [{}]."
                    .format( str(error) )
                )
                return None
        return quince_sqlite( env )


    def __init__( self, env ):
        self._flags = {}
        if cuppa.output_processor.command_available( "pkg-config"):
            command = "pkg-config --cflags --libs sqlite3"
            cflags = subprocess.check_output( shlex.split( command ), stderr=subprocess.STDOUT ).strip()
            self._flags = env.ParseFlags( cflags )
            if 'CPPPATH' in self._flags:
                self._flags['SYSINCPATH'] = self._flags['CPPPATH']
                del self._flags['CPPPATH']

            if 'LIBS' in self._flags:
                self._flags['DYNAMICLIBS'] = self._flags['LIBS']
                del self._flags['LIBS']

        if not 'INCPATH' in self._flags:
            self._flags['INCPATH'] = []
        self._flags['INCPATH'].append( os.path.join( self._location.local(), "include" ) )

        self._src_path = os.path.join( self._location.local(), "src" )

        env.AddMethod( QuinceSqliteLibraryMethod( self._location.local(), self._src_path ), "QuinceSqliteLibrary" )


    def __call__( self, env, toolchain, variant ):

        for name, flags in self._flags.iteritems():
            if flags:
                env.AppendUnique( **{ name: flags } )

        quince_sqlite_lib = env.QuinceSqliteLibrary('static')
        quince_lib = env.QuinceLibrary('static')

        env.Append( STATICLIBS  = [
                quince_sqlite_lib,
                quince_lib,
                env.BoostStaticLibs( [
                    'date_time',
                    'filesystem',
                ] ),
        ] )


    @classmethod
    def name( cls ):
        return cls._name

    def version( self ):
        return str(self._location.version())

    def repository( self ):
        return self._location.repository()

    def branch( self ):
        return self._location.branch()

    def revisions( self ):
        return self._location.revisions()
