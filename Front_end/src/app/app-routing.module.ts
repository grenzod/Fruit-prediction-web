import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './Component/app.component';
import { CamComponent } from './cam/cam.component';

const routes: Routes = [
  { path: '', component: AppComponent },
  { path: 'cam', component: CamComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
