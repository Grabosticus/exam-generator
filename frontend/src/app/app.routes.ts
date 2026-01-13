import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { HomeComponent } from './features/home/home.component';
import { CourseComponent } from './features/course/course.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'course/:id', component: CourseComponent },
    { path: '**', redirectTo: ''}
];
