-- -*- coding: utf-8 -*-
-- <carbontube - distributed pipeline framework>
--
-- Copyright (C) <2016>  Gabriel Falcão <gabriel@nacaolivre.org>
-- (C) Author: Gabriel Falcão <gabriel@nacaolivre.org>
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
local pipeline_name = ARGV[1]; -- a string

-- keys
local key = "carbontube:pipe[" .. pipeline_name .. "]:jobs";
local query = "carbontube:pipe[" .. pipeline_name .. "]:jobs-by-type:*";
local by_id_key = "carbontube:jobs-by-id";

local jobs = {};

local job_id = redis.call("LPOP", key)

for key, queue in pairs(redis.call('KEYS', query)) do
   redis.call("LREM", queue, 0, job_id)
end

return redis.call("HGET", by_id_key, job_id)
