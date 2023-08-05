/**
 * Copyright 2015 Kitware Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Define tasks that build sphinx documentation.
 */
module.exports = function (grunt) {
    grunt.config.merge({
        shell: {
            sphinx: {
                command: [
                    'cd docs',
                    'make html'
                ].join('&&'),
                options: {
                    stdout: true
                }
            },
            sphinx_clean: {
                command: [
                    'cd docs',
                    'make clean'
                ].join('&&'),
                options: {
                    stdout: true
                }
            }
        },

        watch: {
            sphinx: {
                files: ['docs/*.rst'],
                tasks: ['docs']
            }
        }
    });

    grunt.registerTask('docs', function (target) {
        var tasks = ['shell:sphinx'];
        if (target === 'clean') {
            tasks.unshift('shell:sphinx_clean');
        }
        grunt.task.run(tasks);
    });
};
