<?php

class CourseController extends ControllerBase
{

    public function viewAction($code)
    {
        $code = preg_replace("/[^a-zA-Z0-9]+/", "", $code);
        $path = __DIR__ . "/../../../../courses/$code.html";
        $meta = $this->getCourseByCode($code);

        if ($meta == null) {
            $this->view->setVar("title", "404 not found");
        } else {
            $this->view->setVar("title", $meta->korteNaamCursus ?? "");
        }

        $this->view->setVar("code", $code);

        if (file_exists($path) && $course = file_get_contents($path)) {
            $this->view->setVar("course", $course);
            $this->view->setVar("title", $meta->korteNaamCursus ?? "");
        } else {
            $this->view->setVar("course", "<h3>404 - Course not found (stop trying to manipulate the urls, dickhead)</h3>");
            $this->response->setStatusCode(404);
        }
    }

}

