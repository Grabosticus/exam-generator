import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { delay, map } from 'rxjs/operators';

export interface Course {
  course_id: number;
  name: string;
}

@Injectable({
  providedIn: 'root'
})
export class MockCourseService {

  private courses: Course[] = [
    { course_id: 1, name: 'Mathematik' },
    { course_id: 2, name: 'Physik' },
    { course_id: 3, name: 'Chemie' },
    { course_id: 4, name: 'Informatik' },
    { course_id: 5, name: 'Biologie' },
    { course_id: 6, name: 'Englisch' },
    { course_id: 7, name: 'Geschichte' }
  ];

  private nextId = 8;

  constructor() {}

  // GET /courses
  getCourses(): Observable<Course[]> {
    // Mit delay, damit es wie echtes Backend wirkt
    return of(this.courses).pipe(delay(300));
  }

  // POST /courses
  addCourse(course: Partial<Course>): Observable<Course> {
    const newCourse: Course = {
      course_id: this.nextId++,
      name: course.name || 'Neuer Kurs'
    };
    return of(newCourse).pipe(delay(200));
  }

  // GET /courses/:id
  getCourse(course_id: number): Observable<Course | undefined> {
    return of(this.courses.find(c => c.course_id === course_id)).pipe(delay(200));
  }
}
