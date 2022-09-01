import { Component, OnInit } from '@angular/core';
import { ResponseItemsModel } from 'src/app/shared/models/ResponseItemsModel';
import { SkillModel } from 'src/app/shared/models/SkillModel';
import { ProfileService } from 'src/app/shared/services/profile.service';
import { SkillService } from 'src/app/shared/services/skill.service';

@Component({
  selector: 'app-topic',
  templateUrl: './topic.component.html',
  styleUrls: ['./topic.component.css'],
})
export class TopicComponent implements OnInit {
  constructor(private skillService: SkillService) {}
  skills: SkillModel[] = [];
  ngOnInit(): void {
    this.skillService.GetSkills().subscribe((result) => {
      this.skills = result
        ? (result as ResponseItemsModel<SkillModel>).items
        : [];
    });
  }
}
