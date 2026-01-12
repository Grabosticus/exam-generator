import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Course {
  course_id: number;
  name: string;
}

@Injectable({
  providedIn: 'root'
})
export class CourseService {

  private apiUrl = 'http://localhost:8000/courses';

  constructor(private http: HttpClient) { }

  // GET /courses
  getCourses(): Observable<Course[]> {
    return this.http.get<Course[]>(this.apiUrl);
  }

  // POST /courses
  addCourse(name: string): Observable<Course> {
    return this.http.post<Course>(this.apiUrl, {name});
  }

  // GET /courses/COURSe_ID
  getCourse(course_id: number){
    return this.http.get<Course>(`${this.apiUrl}/${course_id}`);
  }
}
