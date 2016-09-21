<?php

class IndexController extends ControllerBase
{

    public function indexAction()
    {
        $this->view->setVar('courses', $this->getCourses());
    }

}

