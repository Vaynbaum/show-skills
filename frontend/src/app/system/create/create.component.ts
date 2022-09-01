import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import axios from 'axios';
import { UnloadContentModel } from 'src/app/shared/models/ContentUnloadModel';
import { ResponseItemsModel } from 'src/app/shared/models/ResponseItemsModel';
import { SkillModel } from 'src/app/shared/models/SkillModel';
import { UnloadPostModel } from 'src/app/shared/models/unloadPostModel';
import { AuthService } from 'src/app/shared/services/auth.service';
import { url } from 'src/app/shared/services/config';
import { PostService } from 'src/app/shared/services/post.service';
import { SkillService } from 'src/app/shared/services/skill.service';

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.css'],
})
export class CreateComponent implements OnInit {
  skills: SkillModel[] = [];

  form: FormGroup = new FormGroup({
    name: new FormControl(null, [Validators.required]),
    skill: new FormControl(null, [Validators.required]),
  });

  urlImage: any;
  ckeditorContent: string = '';
  image: any;
  constructor(
    private postService: PostService,
    private skillService: SkillService
  ) {}
  ngOnInit(): void {
    this.skillService.GetSkills().subscribe((result) => {
      this.skills = result
        ? (result as ResponseItemsModel<SkillModel>).items
        : [];
    });
  }

  fileChange(event: any) {
    let fileList: FileList = event.target.files;
    if (!fileList.length) {
      return;
    }
    this.image = fileList[0];
  }

  async unloadImage() {
    this.postService.UnloadImage(this.image).subscribe((result) => {
      this.urlImage = result;
    });
  }

  unloadPost() {
    const { name, skill } = this.form.value;
    this.postService
      .UnloadContent(new UnloadContentModel(this.ckeditorContent, name))
      .subscribe(
        (result) => {
          this.postService
            .UnloadPost(
              new UnloadPostModel(name, result as string, this.skills[skill])
            )
            .subscribe(
              (result) => {
                console.log('Successfully');
              },
              (err) => {
                console.log(err);
              }
            );
        },
        (err) => {
          console.log(err);
        }
      );
  }
}
