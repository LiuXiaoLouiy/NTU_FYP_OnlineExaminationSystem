import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { UserListComponent } from './user-list/user-list.component';
import { UserAddComponent } from './user-add/user-add.component';
import { UserEditComponent } from './user-edit/user-edit.component';
import { UserDetailComponent } from './user-detail/user-detail.component';
import { UserLoginComponent } from './user-login/user-login.component';
import { ExamListComponent } from './exam-list/exam-list.component';
import { ExamAddComponent } from './exam-add/exam-add.component';
import { ExamEditComponent } from './exam-edit/exam-edit.component';
import { ExamDetailComponent } from './exam-detail/exam-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'user', component: UserListComponent },
  { path: 'detail/:id', component: UserDetailComponent },
  { path: 'edit/:id', component: UserEditComponent },
  { path: 'add', component: UserAddComponent },
  { path: 'login', component: UserLoginComponent },
  { path: 'examlist', component: ExamListComponent },
  { path: 'examadd', component: ExamAddComponent },
  { path: 'examedit/:id', component: ExamEditComponent },
  { path: 'exam/:id', component: ExamDetailComponent }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
