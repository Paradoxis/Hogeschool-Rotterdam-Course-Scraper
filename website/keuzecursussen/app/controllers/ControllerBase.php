<?php

use Phalcon\Mvc\Controller;

class ControllerBase extends Controller
{

    protected function getCourseByCode($code)
    {
        foreach ($this->getCourses() as $course)
        {
            if (isset($course->cursuscode) && $course->cursuscode == $code)
            {
                return $course;
            }
        }

        return null;
    }

    protected function getCourses(): array
    {
        return json_decode(file_get_contents(__DIR__.'/../../../../courses.json'));
    }
}
