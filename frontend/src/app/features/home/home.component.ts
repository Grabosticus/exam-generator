import { Component, OnInit } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import {FormsModule } from '@angular/forms';
import { CourseService, Course } from '../../services/course.service';


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NgFor, RouterModule, NgIf, FormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  courses: Course[] = [];     //all courses
  searchTerm = '';
  filteredCourses: Course[] = [];
  showAddModal = false;
  newCourseName = '';

  constructor(private router: Router, private courseService: CourseService) {}

  ngOnInit(): void {
    this.loadCourses();
  }

  loadCourses() {
    this.courseService.getCourses().subscribe({
      next: data => {
        this.courses = data;
        this.filteredCourses = data;
      },
      error: err => console.error('Error loading courses', err)
    })
  }

  filterCourses() {
    this.filteredCourses = this.courses.filter(course =>
      course.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  openAddModal() {
    this.showAddModal = true;
  }

  closeAddModal() {
    this.showAddModal= false;
    this.newCourseName = '';
  }

  addCourse() {
    if (!this.newCourseName.trim()) return;

    this.courseService.addCourse(this.newCourseName).subscribe({
      next: course => {
        this.courses.push(course);
        this.closeAddModal();

        this.router.navigate(['/course', course.course_id]);
      },
      error: err => console.error('error while adding new course', err)
    });


  }
}



