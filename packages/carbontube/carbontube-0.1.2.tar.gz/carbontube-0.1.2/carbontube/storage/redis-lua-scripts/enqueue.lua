-- -*- coding: utf-8 -*-
-- <carbontube - distributed pipeline framework>
--
-- (C) Copyright <2016>  Gabriel Falcão <gabriel@nacaolivre.org>
-- (C) Author Gabriel Falcão <gabriel@nacaolivre.org>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Lesser General Public License as
-- published by the Free Software Foundation, either version 3 of the
-- License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.

-- args
local job_id = ARGV[1]; -- a sha1hash
local job_type = ARGV[2]; -- a string
local pipeline_name = ARGV[3]; -- a string
local job_data = ARGV[4]; -- the serialized job metadata (that once was a python dict)

-- keys
-- local queue_name      = "carbontube:global:jobs";
-- local type_queue_name = "carbontube:global:jobs-by-type:" .. job_type;

local pipe_queue_name = "carbontube:pipe[" .. pipeline_name .. "]:jobs";
local pipe_type_queue_name = "carbontube:pipe[" .. pipeline_name .. "]:jobs-by-type:" .. job_type;

local by_id_queue_name = "carbontube:jobs-by-id";


local res3 = redis.call("RPUSH", pipe_queue_name, job_id)
local res4 = redis.call("RPUSH", pipe_type_queue_name, job_id)
local res5 = redis.call("HSET", by_id_queue_name, job_id, job_data)

return {
   pipe_queue_name,
   pipe_type_queue_name,
   by_id_queue_name
}
