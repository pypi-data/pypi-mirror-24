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
local pipeline_name = ARGV[1]; -- a string
local job_type = ARGV[2]; -- a string

local key = "carbontube:pipe[" .. pipeline_name .. "]:jobs-by-type:" .. job_type;
local by_id_key = "carbontube:jobs-by-id";

-- local res2 = redis.call("LPUSH", type_queue_name, job_id)
local job_ids = redis.call("LRANGE", key, 0, -1)

local jobs = {};

for key,job_id in pairs(job_ids) do

   jobs[key] = redis.call("HGET", by_id_key, job_id)
end

return jobs
