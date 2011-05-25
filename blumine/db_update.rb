#!/usr/bin/ruby1.8

require 'rubygems'
require  'sqlite3'

print $*[0]

db = SQLite3::Database.new( $*[0] )
columns, *rows = db.execute2( "select * from issues" )

# or use a block:
db.execute2( "select * from issues" ) do |row|
if columns.nil?
    columns = row
else
      # process row
	  print row
end
end
