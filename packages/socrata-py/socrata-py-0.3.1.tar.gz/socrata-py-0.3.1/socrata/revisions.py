import json
import requests
from socrata.http import post, put, delete, get
from socrata.resource import Collection, Resource
from socrata.sources import Source
from socrata.job import Job
import webbrowser

class Revisions(Collection):
    def __init__(self, fourfour, auth):
        self.auth = auth
        self.fourfour = fourfour


    def path(self):
        return 'https://{domain}/api/publishing/v1/revision/{fourfour}'.format(
            domain = self.auth.domain,
            fourfour = self.fourfour
        )

    def _create(self, action_type, metadata):
        body = {
            'metadata': metadata,
            'action': {
                'type': action_type
            }
        }
        return self._subresource(Revision, post(
            self.path(),
            auth = self.auth,
            data = json.dumps(body)
        ))

    def list(self):
        """
        List all the revisions on the view

        Returns:
        ```
            result (bool, dict | list[Revision])
        ```
        """
        return self._subresources(Revision, get(
            self.path(),
            auth = self.auth
        ))


    def create_replace_revision(self, metadata = {}):
        """
        Create a revision on the view, which when applied, will replace the data.

        Args:
        ```
            metadata (dict): The metadata to change; these changes will be applied when the revision
                is applied
        ```
        Returns:
        ```
            result (bool, dict | Revision): The new revision, or an error
        ```
        Examples:
        ```
            >>> view.revisions.create_replace_revision({'name': 'new dataset name', 'description': 'updated description'})
        ```
        """
        return self._create('replace', metadata)

    def create_update_revision(self, metadata = {}):
        """
        Create a revision on the view, which when applied, will update the data
        rather than replacing it.

        This is an upsert; if there is a rowId defined and you have duplicate ID values,
        those rows will be updated. Otherwise they will be appended.

        Args:
        ```
            metadata (dict): The metadata to change; these changes will be applied when the revision is applied
        ```

        Returns:
        ```
            result (bool, dict | Revision): The new revision, or an error
        ```

        Examples:
        ```python
            view.revisions.create_update_revision({
                'name': 'new dataset name',
                'description': 'updated description'
            })
        ```
        """
        return self._create('update', metadata)

    @staticmethod
    def new(auth, metadata):
        path = 'https://{domain}/api/publishing/v1/revision'.format(
            domain = auth.domain,
        )

        (ok, response) = result = post(
            path,
            auth = auth,
            data = json.dumps({
                'action': {
                    'type': 'update'
                },
                'metadata': metadata
            })
        )

        if not ok:
            return result

        return (ok, Revision(auth, response))

    def lookup(self, revision_seq):
        """
        Lookup a revision within the view based on the sequence number

        Args:
        ```
            revision_seq (int): The sequence number of the revision to lookup
        ```

        Returns:
        ```
            result (bool, dict | Revision): The Revision resulting from this API call, or an error
        ```
        """
        return self._subresource(Revision, get(
            self.path() + '/' + str(revision_seq),
            auth = self.auth
        ))

    def create_using_config(self, config):
        """
        Create a revision for the given dataset.
        """
        return self._subresource(Revision, post(
            self.path(),
            auth = self.auth,
            data = json.dumps({
                'config': config.attributes['name']
            })
        ))


class Revision(Resource):
    """
    A revision is a change to a dataset
    """

    def create_upload(self, filename):
        """
        Create an upload within this revision

        Args:
        ```
            filename (str): The name of the file to upload
        ```
        Returns:
        ```
            result (bool, dict | Source): The Source created by this API call, or an error
        ```
        """
        return self.create_source({
            'type': 'upload',
            'filename': filename
        })

    def create_source(self, uri, source_type):
        return self._subresource(Source, post(
            self.path(uri),
            auth = self.auth,
            data = json.dumps({
                'source_type' : source_type
            })
        ))

    def discard(self, uri):
        """
        Discard this open revision.

        Returns:
        ```
            result (bool, dict | Revision): The closed Revision or an error
        ```
        """
        return delete(self.path(uri), auth = self.auth)


    def update(self, uri, meta):
        """
        Set the metadata to be applied to the view
        when this revision is applied

        Args:
        ```
            metadata (dict): The changes to make to this revision
        ```

        Returns:
        ```
            result (bool, dict | Revision): The updated Revision as a result of this API call, or an error
        ```

        Examples:
        ```python
            (ok, revision) = revision.update({
                'name': 'new name',
                'description': 'new description'
            })
        ```
        """
        return self._mutate(put(
            self.path(uri),
            auth = self.auth,
            data = json.dumps({'metadata': meta}),
        ))

    def apply(self, uri, output_schema = None):
        """
        Apply the Revision to the view that it was opened on

        Args:
        ```
            output_schema (OutputSchema): Optional output schema. If your revision includes
                data changes, this should be included. If it is a metadata only revision,
                then you will not have an output schema, and you do not need to pass anything
                here
        ```

        Returns:
        ```
            result (bool, dict | Job): Returns the job that is being run to apply the revision
        ```

        Examples:
        ```
        (ok, job) = revision.apply(output_schema = my_output_schema)
        ```
        """

        if output_schema:
            (ok, output_schema) = result = output_schema.wait_for_finish()
            if not ok:
                return result

        body = {}

        if output_schema:
            body.update({
                'output_schema_id': output_schema.attributes['id']
            })

        result = self._subresource(Job, put(
            self.path(uri),
            auth = self.auth,
            data = json.dumps(body)
        ))

        self.show() # To mutate ourself and get the job to show up in our attrs

        return result

    def ui_url(self):
        """
        This is the URL to the landing page in the UI for this revision

        Returns:
        ```
            url (str): URL you can paste into a browser to view the revision UI
        ```
        """
        return "https://{domain}/d/{fourfour}/manage/revisions/{seq}".format(
            domain = self.auth.domain,
            fourfour = self.attributes["fourfour"],
            seq = self.attributes["revision_seq"]
        )

    def open_in_browser(self):
        """
        Open this revision in your browser, this will open a window
        """
        webbrowser.open(self.ui_url(), new = 2)

    def view_id(self):
        return self.attributes["fourfour"]
